// 立即执行函数，添加控制台输出确认执行
(function() {
  console.log("首页动画脚本已加载"); // 打开控制台查看是否有此输出

  // 等待DOM加载完成
  document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM加载完成，准备执行动画");

    const splashScreen = document.querySelector('.custom-splash-screen');
    const dynamicTitle = document.querySelector('.custom-dynamic-title');
    const dynamicSubtitle = document.querySelector('.custom-dynamic-subtitle');
    const homeMain = document.querySelector('.custom-home-main');

    // 输出元素查找结果，确认是否找到
    console.log("开屏容器:", splashScreen);
    console.log("标题元素:", dynamicTitle);

    if (!splashScreen || !dynamicTitle) {
      console.error("未找到动画元素，请检查类名是否正确");
      return;
    }

    // 立即触发动画（去掉延迟，快速测试）
    dynamicTitle.style.opacity = '1';
    dynamicTitle.style.transform = 'translateY(0)';
    dynamicSubtitle.style.opacity = '1';
    dynamicSubtitle.style.transform = 'translateY(0)';

    // 2秒后隐藏开屏
    setTimeout(() => {
      splashScreen.classList.add('fade-out');
      homeMain.classList.add('show');
      console.log("动画执行完成");
    }, 2000);
  });
})();