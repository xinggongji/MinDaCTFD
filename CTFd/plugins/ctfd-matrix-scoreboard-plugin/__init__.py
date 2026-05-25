import os
from datetime import datetime  # 新增：用于处理时间
from flask import (
    render_template, jsonify, Blueprint, url_for, session, redirect, request
)
from sqlalchemy.sql import or_, func  # 新增：用于聚合查询
from CTFd import utils, scoreboard
from CTFd.models import db, Solves, Challenges, Teams, Users  # 新增：Teams/Users模型
from CTFd.plugins import override_template
from CTFd.utils.config import is_scoreboard_frozen, ctf_theme, is_users_mode
from CTFd.utils.config.visibility import challenges_visible, scores_visible
from CTFd.utils.dates import (
    ctf_started, ctftime, view_after_ctf, unix_time_to_utc
)
from CTFd.utils.user import is_admin, authed, get_current_user  # 新增：获取当前用户


def load(app):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'scoreboard-matrix.html')
    override_template('scoreboard.html', open(template_path).read())
    # 新增：个人详情页模板
    user_detail_template = os.path.join(dir_path, 'user-detail.html')
    override_template('user_detail.html', open(user_detail_template).read())

    matrix = Blueprint('matrix', __name__, static_folder='static')
    app.register_blueprint(matrix, url_prefix='/matrix')

    # 新增：获取所有题目类型
    def get_categories():
        categories = db.session.query(Challenges.category).distinct().all()
        return [c[0] for c in categories if c[0]]  # 过滤空类型

    # 改造：支持按类型筛选题目
    def get_challenges(category=None):
        if not is_admin():
            if not ctftime() and not view_after_ctf():
                return []
        query = db.session.query(
            Challenges.id,
            Challenges.name,
            Challenges.category
        ).filter(or_(Challenges.state != 'hidden', Challenges.state is None))
        if category:  # 新增：按类型筛选
            query = query.filter(Challenges.category == category)
        chals = query.all()
        jchals = [{'id': x.id, 'name': x.name, 'category': x.category} for x in chals]
        # 按类型分组排序
        categories = set(c['category'] for c in jchals)
        return [c for cat in categories for c in jchals if c['category'] == cat]

    # 改造：支持按类型计算排名（总分/类型分），兼容团队/个人模式
    def get_standings(category=None):
        if is_users_mode():
            # 个人模式：按 user_id 聚合
            query = db.session.query(
                Solves.user_id,
                Users.name,
                func.sum(Challenges.value).label('score'),
                func.count(Solves.id).label('solve_count'),
                func.max(Solves.date).label('last_solve_time')
            ).join(Challenges, Solves.challenge_id == Challenges.id
            ).join(Users, Solves.user_id == Users.id)

            if category:
                query = query.filter(Challenges.category == category)

            freeze = utils.get_config('freeze')
            if freeze and not is_admin():
                freeze_time = unix_time_to_utc(freeze)
                query = query.filter(Solves.date < freeze_time)

            standings = query.group_by(Solves.user_id, Users.name).order_by(
                func.sum(Challenges.value).desc(),
                func.count(Solves.id).asc()
            ).all()

            result = []
            for idx, standing in enumerate(standings):
                user_id, name, score, solve_count, last_time = standing
                solves = db.session.query(Solves.challenge_id
                ).filter(Solves.user_id == user_id).all()
                solve_ids = [s[0] for s in solves]
                result.append({
                    'rank': idx + 1,
                    'teamid': user_id,
                    'name': name,
                    'score': score or 0,
                    'solve_count': solve_count,
                    'last_solve_time': last_time.strftime('%Y-%m-%d %H:%M:%S') if last_time else None,
                    'solves': solve_ids
                })
            return result
        else:
            # 团队模式：按 team_id 聚合
            query = db.session.query(
                Solves.team_id,
                Teams.name,
                func.sum(Challenges.value).label('score'),
                func.count(Solves.id).label('solve_count'),
                func.max(Solves.date).label('last_solve_time')
            ).join(Challenges, Solves.challenge_id == Challenges.id
            ).join(Teams, Solves.team_id == Teams.id)

            if category:
                query = query.filter(Challenges.category == category)

            freeze = utils.get_config('freeze')
            if freeze and not is_admin():
                freeze_time = unix_time_to_utc(freeze)
                query = query.filter(Solves.date < freeze_time)

            standings = query.group_by(Solves.team_id, Teams.name).order_by(
                func.sum(Challenges.value).desc(),
                func.count(Solves.id).asc()
            ).all()

            result = []
            for idx, standing in enumerate(standings):
                team_id, name, score, solve_count, last_time = standing
                solves = db.session.query(Solves.challenge_id
                ).filter(Solves.team_id == team_id).all()
                solve_ids = [s[0] for s in solves]
                result.append({
                    'rank': idx + 1,
                    'teamid': team_id,
                    'name': name,
                    'score': score or 0,
                    'solve_count': solve_count,
                    'last_solve_time': last_time.strftime('%Y-%m-%d %H:%M:%S') if last_time else None,
                    'solves': solve_ids
                })
            return result

    # 新增：获取个人详细信息
    def get_user_details(user_id):
        user = Users.query.get(user_id)
        if not user:
            return None
        # 获取所属团队
        team = Teams.query.filter_by(id=user.team_id).first() if user.team_id else None
        # 个人解题记录
        solves = db.session.query(
            Solves.challenge_id,
            Challenges.name,
            Challenges.category,
            Solves.date
        ).join(Challenges, Solves.challenge_id == Challenges.id
        ).filter(Solves.user_id == user_id
        ).order_by(Solves.date.desc()).all()
        return {
            'user': user,
            'team': team,
            'solves': [{
                'chal_id': s[0],
                'chal_name': s[1],
                'category': s[2],
                'solve_time': s[3].strftime('%Y-%m-%d %H:%M:%S')
            } for s in solves],
            'solve_count': len(solves)
        }

    # 改造：支持按类型显示计分板
    def scoreboard_view():
        if not scores_visible():
            return render_template('scoreboard.html', errors=['分数当前不可见'])
        if not authed() and scores_visible():
            return redirect(url_for('auth.login', next=request.path))
        
        category = request.args.get('category')  # 获取类型参数
        standings = get_standings(category)
        challenges = get_challenges(category)
        categories = get_categories()  # 所有类型用于导航
        
        return render_template('scoreboard.html',
                               standings=standings,
                               challenges=challenges,
                               categories=categories,  # 传递类型列表
                               current_category=category,  # 当前类型
                               score_frozen=is_scoreboard_frozen(),
                               mode='users' if is_users_mode() else 'teams',
                               theme=ctf_theme())

    # 新增：个人详情页视图
    def user_detail_view(user_id):
        if not authed():
            return redirect(url_for('auth.login', next=request.path))
        details = get_user_details(user_id)
        if not details:
            return render_template('user_detail.html', errors=['用户不存在'])
        return render_template('user_detail.html', **details)

    # 改造：分数接口支持类型筛选
    def scores():
        if not scores_visible():
            return jsonify({'standings': []})
        category = request.args.get('category')
        standings = get_standings(category)
        return jsonify({
            'standings': [{
                'pos': s['rank'],
                'id': s['teamid'],
                'team': s['name'],
                'score': s['score'],
                'solve_count': s['solve_count'],
                'last_solve_time': s['last_solve_time']
            } for s in standings]
        })

    # 注册路由
    app.view_functions['scoreboard.listing'] = scoreboard_view
    app.view_functions['scoreboard.score'] = scores
    app.add_url_rule('/user/<int:user_id>', 'user_detail', user_detail_view)  # 个人详情页路由