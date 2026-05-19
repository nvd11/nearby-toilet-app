const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 2
  });
  console.log('Navigating...');
  await page.goto('https://github.com/torvalds/linux');
  
  await page.waitForTimeout(4000);
  
  console.log('Highlighting...');

  const highlightScript = (el) => {
      el.style.border = '4px solid red';
      el.style.borderRadius = '6px';
      el.style.boxShadow = '0 0 15px red';
      el.style.position = 'relative';
      el.style.zIndex = '9999';
      
      const label = document.createElement('div');
      label.textContent = '👆 Click Here to Fork!';
      label.style.position = 'absolute';
      label.style.top = '100%';
      label.style.right = '0';
      label.style.backgroundColor = 'red';
      label.style.color = 'white';
      label.style.padding = '4px 8px';
      label.style.borderRadius = '4px';
      label.style.fontSize = '14px';
      label.style.whiteSpace = 'nowrap';
      label.style.marginTop = '4px';
      el.appendChild(label);
  };

  try {
      // GitHub usually uses an element with id fork-button
      await page.locator('#fork-button').evaluate(highlightScript);
      console.log('Highlighted #fork-button');
  } catch (e) {
      console.log('Could not find #fork-button, trying fallback...');
      try {
          await page.locator('a[href$="/fork"]').first().evaluate(highlightScript);
          console.log('Highlighted a[href$="/fork"]');
      } catch (e2) {
          console.log('Could not find by href either.');
      }
  }

  console.log('Taking screenshot...');
  await page.screenshot({ path: '/home/gateman/.openclaw/workspace/github_fork_real.png' });
  await browser.close();
  console.log('Done!');
})();