/**
 * MCP Shrimp Task Manager 網站主腳本
 */

// 頁面加載完成後執行
document.addEventListener("DOMContentLoaded", function () {
  // 初始化滾動動畫
  initAOS();

  // 初始化移動端菜單
  initMobileMenu();

  // 初始化代碼高亮和複製功能
  initCodeBlocks();

  // 平滑滾動功能
  initSmoothScroll();

  // 英雄區特效
  initHeroEffects();

  // 痛點與解決方案區特效
  initPainPointsEffects();

  // 核心功能展示區特效
  initFeaturesEffects();

  // 工作流程展示區特效
  initWorkflowEffects();

  // 初始化安裝與配置區功能
  initInstallationSection();

  // 檢測頁面滾動位置以顯示回到頂部按鈕
  initScrollToTopButton();

  // 初始化響應式圖片懶加載
  initLazyLoading();

  // 初始化頁面進入動畫
  initPageEntranceAnimation();

  // 多語系功能
  initMultiLanguage();
});

/**
 * 初始化AOS滾動動畫庫
 */
function initAOS() {
  AOS.init({
    duration: 800,
    easing: "ease-in-out",
    once: true,
    mirror: true,
    disable: function () {
      // 只在低性能設備上禁用動畫，根據用戶偏好設置
      return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    },
  });

  // 在窗口調整大小時重新初始化AOS以確保正確的觸發位置
  window.addEventListener("resize", function () {
    AOS.refresh();
  });
}

/**
 * 初始化移動端菜單
 */
function initMobileMenu() {
  const menuToggle = document.getElementById("menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");

  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener("click", function (e) {
      e.preventDefault();

      // 為了支持過渡效果，先移除hidden類
      if (mobileMenu.classList.contains("hidden")) {
        mobileMenu.classList.remove("hidden");

        // 等待DOM更新，然後添加visible類啟動過渡效果
        setTimeout(() => {
          mobileMenu.classList.add("visible");
        }, 10);
      } else {
        // 先移除visible類觸發過渡效果
        mobileMenu.classList.remove("visible");

        // 等待過渡完成，然後隱藏菜單
        setTimeout(() => {
          mobileMenu.classList.add("hidden");
        }, 300); // 300ms與CSS過渡時間匹配
      }
    });

    // 點擊菜單項後關閉菜單
    const menuLinks = mobileMenu.querySelectorAll("a");
    menuLinks.forEach((link) => {
      link.addEventListener("click", function () {
        mobileMenu.classList.remove("visible");

        // 等待過渡完成，然後隱藏菜單
        setTimeout(() => {
          mobileMenu.classList.add("hidden");
        }, 300);
      });
    });

    // 點擊菜單外區域關閉菜單
    document.addEventListener("click", function (e) {
      if (
        !menuToggle.contains(e.target) &&
        !mobileMenu.contains(e.target) &&
        !mobileMenu.classList.contains("hidden")
      ) {
        mobileMenu.classList.remove("visible");

        setTimeout(() => {
          mobileMenu.classList.add("hidden");
        }, 300);
      }
    });
  }
}

/**
 * 英雄區特效初始化
 */
function initHeroEffects() {
  // 獲取英雄區
  const heroSection = document.getElementById("hero");
  if (!heroSection) return;

  // 添加浮動裝飾元素的動畫序列
  const decorElements = heroSection.querySelectorAll(".absolute");
  decorElements.forEach((elem, index) => {
    elem.style.setProperty("--animation-order", index + 1);

    // 使用淡入動畫讓元素在頁面加載後逐個顯示
    setTimeout(() => {
      elem.style.opacity = "0.8";
    }, (index + 1) * 200);
  });

  // 添加視差滾動效果
  window.addEventListener("scroll", function () {
    const scrollTop = window.pageYOffset;
    const heroHeight = heroSection.offsetHeight;

    // 當用戶滾動經過英雄區時應用效果
    if (scrollTop <= heroHeight) {
      const scrollPercentage = scrollTop / heroHeight;

      // 英雄區域淡出效果
      heroSection.style.opacity = 1 - scrollPercentage * 0.8;

      // 標題向上移動效果
      const heroTitle = heroSection.querySelector("h1");
      if (heroTitle) {
        heroTitle.style.transform = `translateY(${scrollPercentage * 50}px)`;
      }
    }
  });

  // 添加滑鼠移動視差效果
  heroSection.addEventListener("mousemove", function (e) {
    // 只在更大的屏幕上啟用這個效果
    if (window.innerWidth >= 768) {
      const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
      const moveY = (e.clientY - window.innerHeight / 2) * 0.01;

      // 獲取英雄區內的圖片元素
      const heroImage = heroSection.querySelector("img");
      if (heroImage) {
        heroImage.style.transform = `translate(${moveX * 2}px, ${
          moveY * 2
        }px) scale(1.02)`;
      }

      // 獲取英雄區內的裝飾元素
      decorElements.forEach((elem, index) => {
        // 使用不同的移動比例，創造層次感
        const factorX = (index + 1) * 0.03;
        const factorY = (index + 1) * 0.02;
        elem.style.transform = `translate(${moveX * factorX}px, ${
          moveY * factorY
        }px)`;
      });
    }
  });

  // 鼠標離開時重置元素位置
  heroSection.addEventListener("mouseleave", function () {
    const heroImage = heroSection.querySelector("img");
    if (heroImage) {
      heroImage.style.transform = "";
    }

    decorElements.forEach((elem) => {
      elem.style.transform = "";
    });
  });

  // Logo動畫效果
  const logo = document.querySelector("header nav img");
  if (logo) {
    // 導航欄 logo 在頁面加載時輕微旋轉動畫
    logo.style.transition = "transform 1s ease-out";
    logo.style.transform = "rotate(0deg)";

    setTimeout(() => {
      logo.style.transform = "rotate(5deg)";
      setTimeout(() => {
        logo.style.transform = "rotate(0deg)";
      }, 500);
    }, 1500);
  }
}

/**
 * 痛點與解決方案區特效初始化
 */
function initPainPointsEffects() {
  const painPointsSection = document.getElementById("pain-points");
  if (!painPointsSection) return;

  // 獲取所有卡片
  const cards = painPointsSection.querySelectorAll(
    ".rounded-lg.overflow-hidden"
  );

  // 為每個卡片添加延遲出現動畫
  cards.forEach((card, index) => {
    card.setAttribute("data-aos", "fade-up");
    card.setAttribute("data-aos-delay", (index * 150).toString());
  });

  // 為每個卡片添加鼠標進入和離開效果
  cards.forEach((card, index) => {
    // 獲取痛點和解決方案區塊
    const painIcon = card.querySelector(".p-6 img");
    const solutionIcon = card.querySelector(".p-4 img");
    const arrowIcon = card.querySelector(".h-8.w-8.text-green-500");

    // 鼠標進入效果
    card.addEventListener("mouseenter", function () {
      // 延遲執行動畫，營造序列動畫效果
      if (painIcon) {
        setTimeout(() => {
          painIcon.style.transform = "scale(1.1) rotate(5deg)";
        }, 100);
      }

      if (arrowIcon) {
        setTimeout(() => {
          arrowIcon.style.transform = "translateY(8px)";
        }, 200);
      }

      if (solutionIcon) {
        setTimeout(() => {
          solutionIcon.style.transform = "scale(1.1) rotate(-5deg)";
        }, 300);
      }

      // 添加發光效果
      card.style.boxShadow =
        "0 20px 30px rgba(0, 0, 0, 0.15), 0 0 15px rgba(59, 130, 246, 0.3)";
    });

    // 鼠標離開效果
    card.addEventListener("mouseleave", function () {
      if (painIcon) painIcon.style.transform = "";
      if (arrowIcon) arrowIcon.style.transform = "";
      if (solutionIcon) solutionIcon.style.transform = "";

      // 移除發光效果
      card.style.boxShadow = "";
    });
  });

  // 添加視差滾動效果
  window.addEventListener("scroll", function () {
    // 只在更大的屏幕上啟用這個效果
    if (window.innerWidth >= 768) {
      const scrollPosition = window.scrollY;
      const sectionTop = painPointsSection.offsetTop;
      const sectionHeight = painPointsSection.offsetHeight;

      // 當用戶滾動到該區域時應用效果
      if (
        scrollPosition > sectionTop - window.innerHeight &&
        scrollPosition < sectionTop + sectionHeight
      ) {
        cards.forEach((card, index) => {
          // 相對於部分的滾動位置
          const relativeScroll =
            (scrollPosition - (sectionTop - window.innerHeight)) /
            (sectionHeight + window.innerHeight);
          // 根據卡片位置計算偏移量
          const offset = Math.sin(relativeScroll * Math.PI + index * 0.5) * 15;

          // 根據索引設置不同的偏移方向
          if (index % 2 === 0) {
            card.style.transform = `translateY(${offset}px)`;
          } else {
            card.style.transform = `translateY(${-offset}px)`;
          }
        });
      }
    }
  });
}

/**
 * 初始化代碼區塊功能
 */
function initCodeBlocks() {
  // 確保 Prism.js 已加載
  if (typeof Prism !== "undefined") {
    // 代碼高亮應用
    Prism.highlightAll();
  }

  // 初始化代碼示例切換功能
  initCodeTabSwitcher();

  // 可選：添加打字機效果
  initTypingEffect();
}

/**
 * 初始化代碼示例標籤切換功能
 */
function initCodeTabSwitcher() {
  const tabButtons = document.querySelectorAll(".code-tab-btn");
  const contentSections = document.querySelectorAll(".code-content-section");

  if (!tabButtons.length || !contentSections.length) return;

  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      // 獲取目標內容ID
      const targetId = btn.getAttribute("data-target");

      // 取消所有按鈕激活狀態
      tabButtons.forEach((b) => {
        b.classList.remove("active", "bg-blue-50", "text-blue-600");
        b.classList.add("hover:bg-blue-50");
      });

      // 激活當前按鈕
      btn.classList.add("active", "bg-blue-50", "text-blue-600");

      // 隱藏所有內容
      contentSections.forEach((section) => {
        section.classList.add("hidden");
      });

      // 顯示目標內容
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.remove("hidden");

        // 確保激活內容區的代碼高亮
        const codeBlocks = targetSection.querySelectorAll("code");
        if (typeof Prism !== "undefined" && codeBlocks.length) {
          codeBlocks.forEach((block) => {
            Prism.highlightElement(block);
          });
        }
      }
    });
  });
}

/**
 * 初始化打字機效果 (可選功能)
 */
function initTypingEffect() {
  // 檢查是否啟用打字機效果（可以通過URL參數控制）
  const urlParams = new URLSearchParams(window.location.search);
  const enableTyping = urlParams.get("typing") === "true";

  if (!enableTyping) return;

  const codeBlocks = document.querySelectorAll("#examples code");
  if (!codeBlocks.length) return;

  codeBlocks.forEach((codeBlock) => {
    const originalText = codeBlock.textContent;
    codeBlock.textContent = "";

    let charIndex = 0;
    const typingSpeed = 30; // 每字符間隔毫秒

    // 先隱藏原始代碼，然後進行打字效果
    codeBlock.parentElement.classList.add("typing-in-progress");

    // 視窗進入可視區域時啟動打字效果
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          startTyping();
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(codeBlock.parentElement);

    function startTyping() {
      const typingInterval = setInterval(() => {
        if (charIndex < originalText.length) {
          codeBlock.textContent += originalText.charAt(charIndex);
          charIndex++;

          // 自動滾動代碼塊以跟踪光標
          codeBlock.parentElement.scrollTop =
            codeBlock.parentElement.scrollHeight;

          // 動態應用語法高亮
          if (typeof Prism !== "undefined") {
            Prism.highlightElement(codeBlock);
          }
        } else {
          clearInterval(typingInterval);
          codeBlock.parentElement.classList.remove("typing-in-progress");
        }
      }, typingSpeed);
    }
  });
}

/**
 * 初始化平滑滾動
 */
function initSmoothScroll() {
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href");

      // 確保不是僅 "#" 的鏈接
      if (href !== "#") {
        e.preventDefault();
        const target = document.querySelector(href);

        if (target) {
          // 計算目標元素位置並考慮固定導航欄的高度
          const headerHeight = document.querySelector("header").offsetHeight;
          const targetPosition =
            target.getBoundingClientRect().top +
            window.pageYOffset -
            headerHeight;

          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          });
        }
      }
    });
  });
}

/**
 * 核心功能展示區特效初始化
 */
function initFeaturesEffects() {
  const featuresSection = document.getElementById("features");
  if (!featuresSection) return;

  // 獲取所有功能卡片
  const featureCards = featuresSection.querySelectorAll(".rounded-lg");

  // 為每個卡片添加懸停效果
  featureCards.forEach((card, index) => {
    // 獲取卡片中的圖標和標題
    const featureIcon = card.querySelector(".p-6 img");
    const featureTitle = card.querySelector("h3");

    // 鼠標進入效果
    card.addEventListener("mouseenter", function () {
      if (featureIcon) {
        featureIcon.style.transform = "scale(1.2) rotate(5deg)";
        featureIcon.style.transition = "transform 0.5s ease";
      }

      if (featureTitle) {
        featureTitle.style.transform = "translateY(-5px)";
        featureTitle.style.transition = "transform 0.3s ease";
      }
    });

    // 鼠標離開效果
    card.addEventListener("mouseleave", function () {
      if (featureIcon) {
        featureIcon.style.transform = "";
      }

      if (featureTitle) {
        featureTitle.style.transform = "";
      }
    });

    // 點擊效果 - 添加輕微彈跳效果
    card.addEventListener("click", function () {
      card.style.transform = "scale(0.95)";
      setTimeout(() => {
        card.style.transform = "";
      }, 200);
    });
  });

  // 添加滾動視差效果
  window.addEventListener("scroll", function () {
    const scrollPosition = window.scrollY;
    const windowHeight = window.innerHeight;

    // 計算特效觸發範圍
    const sectionTop = featuresSection.offsetTop;
    const sectionHeight = featuresSection.offsetHeight;
    const triggerStart = sectionTop - windowHeight;
    const triggerEnd = sectionTop + sectionHeight;

    // 只在特效範圍內計算視差
    if (scrollPosition > triggerStart && scrollPosition < triggerEnd) {
      const scrollProgress =
        (scrollPosition - triggerStart) / (triggerEnd - triggerStart);

      // 應用各種視差效果
      featureCards.forEach((card, index) => {
        const delayFactor = (index % 3) * 0.1;
        const moveY = Math.sin((scrollProgress + delayFactor) * Math.PI) * 15;

        // 應用視差效果
        card.style.transform = `translateY(${moveY}px)`;
      });
    }
  });
}

/**
 * 工作流程展示區特效初始化
 */
function initWorkflowEffects() {
  // 步驟詳情彈窗功能
  initWorkflowModal();

  // 為桌面版時間軸添加連接線動畫
  animateWorkflowConnections();

  // 為步驟圖標添加互動效果
  addWorkflowIconInteractions();
}

/**
 * 初始化工作流程詳情彈窗
 */
function initWorkflowModal() {
  const modal = document.getElementById("workflow-detail-modal");
  const closeBtn = document.getElementById("close-modal");
  const closeBtnAlt = document.getElementById("close-modal-btn");
  const detailLinks = document.querySelectorAll(
    ".workflow-detail-link, .workflow-step"
  );
  const modalTitle = document.getElementById("modal-title");
  const modalContent = document.getElementById("modal-content");

  if (!modal || !closeBtn || !detailLinks.length) return;

  // 工作流程步驟詳情數據
  const workflowDetails = {
    en: {
      1: {
        title: "Task Planning",
        content: `
          <p>The task planning stage is the initial phase where AI assistants define project scope, set goals, and establish success criteria.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Clarify project requirements and constraints</li>
            <li>Set clear objectives and define measurable success criteria</li>
            <li>Establish project boundaries and identify stakeholders</li>
            <li>Create a high-level plan with timeline estimates</li>
            <li>Optionally reference existing tasks for continuous planning</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Outputs:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Comprehensive task description</li>
            <li>Clear success criteria</li>
            <li>Technical requirements and constraints</li>
          </ul>
          <p class="mt-4">This stage lays the foundation for all subsequent work, ensuring that both the AI assistant and the user have a shared understanding of what needs to be accomplished.</p>
        `,
      },
      2: {
        title: "In-depth Analysis",
        content: `
          <p>The in-depth analysis stage involves a thorough examination of the requirements and technical landscape to develop a viable implementation strategy.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Analyze requirements and identify technical challenges</li>
            <li>Evaluate technical feasibility and potential risks</li>
            <li>Research best practices and available solutions</li>
            <li>Systematically review existing codebase if applicable</li>
            <li>Develop initial implementation concepts</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Outputs:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Technical feasibility assessment</li>
            <li>Risk identification and mitigation strategies</li>
            <li>Initial implementation approach</li>
            <li>Pseudocode or architectural diagrams where appropriate</li>
          </ul>
          <p class="mt-4">This stage ensures that the proposed solution is technically sound and addresses all requirements before proceeding to implementation.</p>
        `,
      },
      3: {
        title: "Solution Reflection",
        content: `
          <p>The solution reflection stage involves critical review and optimization of the proposed approach before implementation.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Critically review the analysis results and proposed solutions</li>
            <li>Identify potential gaps, edge cases, or inefficiencies</li>
            <li>Consider alternative approaches and their trade-offs</li>
            <li>Evaluate solution against best practices and design principles</li>
            <li>Refine implementation strategy based on insights</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Outputs:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Optimized solution design</li>
            <li>Documented considerations and trade-offs</li>
            <li>Refined implementation strategy</li>
          </ul>
          <p class="mt-4">This reflective process helps catch potential issues early and ensures the chosen approach is optimal before investing in implementation.</p>
        `,
      },
      4: {
        title: "Task Decomposition",
        content: `
          <p>The task decomposition stage breaks down complex tasks into manageable, atomic subtasks with clear dependencies and execution order.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Break down complex tasks into smaller, manageable units</li>
            <li>Establish clear dependencies between subtasks</li>
            <li>Define scope and acceptance criteria for each subtask</li>
            <li>Assign priority levels and estimate complexity</li>
            <li>Create a logical execution sequence</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Supported Update Modes:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li><strong>Append:</strong> Keep all existing tasks and add new ones</li>
            <li><strong>Overwrite:</strong> Clear all uncompleted tasks and completely replace them, while preserving completed tasks</li>
            <li><strong>Selective:</strong> Intelligently update existing tasks based on task names, preserving tasks not in the list</li>
            <li><strong>Clear All Tasks:</strong> Remove all tasks and create a backup</li>
          </ul>
          <p class="mt-4">This structured approach makes complex projects manageable by creating a clear roadmap of small, achievable steps.</p>
        `,
      },
      5: {
        title: "Task Execution",
        content: `
          <p>The task execution stage involves implementing specific tasks according to the predetermined plan, with a focus on quality and adherence to requirements.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Select tasks for execution based on dependencies and priorities</li>
            <li>Implement solutions following the implementation guide</li>
            <li>Follow coding standards and best practices</li>
            <li>Handle edge cases and error conditions</li>
            <li>Document implementation decisions and rationale</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Execution Process:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Prepare necessary resources and environment</li>
            <li>Follow the implementation guide step by step</li>
            <li>Monitor progress and handle any unexpected issues</li>
            <li>Maintain code quality and documentation</li>
          </ul>
          <p class="mt-4">This stage transforms plans into concrete results, implementing the solutions designed in earlier stages.</p>
        `,
      },
      6: {
        title: "Result Verification",
        content: `
          <p>The result verification stage ensures that implemented tasks meet all requirements and quality standards before being marked as complete.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Verify that all requirements have been implemented</li>
            <li>Check for adherence to technical standards and best practices</li>
            <li>Test edge cases and error handling</li>
            <li>Review code quality and documentation</li>
            <li>Validate against the verification criteria defined for the task</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Verification Checklist:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Functional correctness: Does it work as expected?</li>
            <li>Completeness: Are all requirements addressed?</li>
            <li>Quality: Does it meet coding standards and best practices?</li>
            <li>Performance: Does it operate efficiently?</li>
            <li>Documentation: Is the implementation well-documented?</li>
          </ul>
          <p class="mt-4">This thorough verification process ensures high-quality deliverables that fully satisfy requirements.</p>
        `,
      },
      7: {
        title: "Task Completion",
        content: `
          <p>The task completion stage formally marks tasks as complete, generates detailed completion reports, and updates the status of dependent tasks.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Formally mark task as completed after successful verification</li>
            <li>Generate a comprehensive completion report</li>
            <li>Update the status of dependent tasks</li>
            <li>Archive relevant information for future reference</li>
            <li>Communicate completion to stakeholders</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Completion Report Contents:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Summary of completed work</li>
            <li>Implementation highlights and key decisions</li>
            <li>Any notable challenges encountered and their solutions</li>
            <li>Recommendations for future work or improvements</li>
          </ul>
          <p class="mt-4">The completion stage ensures proper closure of tasks, maintains workflow continuity, and builds institutional knowledge for future projects.</p>
        `,
      },
    },
    "zh-TW": {
      1: {
        title: "任務規劃",
        content: `
          <p>任務規劃階段是初始階段，AI助手定義項目範圍、設定目標，並建立成功標準。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>釐清項目需求和約束條件</li>
            <li>設定明確目標和定義可衡量的成功標準</li>
            <li>確立項目界限和識別相關利益方</li>
            <li>創建高級計劃及時間估算</li>
            <li>可選擇參考現有任務進行持續規劃</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">輸出成果：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>全面的任務描述</li>
            <li>明確的成功標準</li>
            <li>技術需求和約束條件</li>
          </ul>
          <p class="mt-4">此階段為所有後續工作奠定基礎，確保AI助手和用戶對需要完成的工作有共同理解。</p>
        `,
      },
      2: {
        title: "深入分析",
        content: `
          <p>深入分析階段涉及對需求和技術環境的徹底檢查，以制定可行的實施策略。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>分析需求並識別技術挑戰</li>
            <li>評估技術可行性和潛在風險</li>
            <li>研究最佳實踐和可用解決方案</li>
            <li>系統性地審查現有代碼庫（如適用）</li>
            <li>開發初步實施概念</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">輸出成果：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>技術可行性評估</li>
            <li>風險識別和緩解策略</li>
            <li>初步實施方法</li>
            <li>適當的偽代碼或架構圖</li>
          </ul>
          <p class="mt-4">此階段確保在進行實施前，提出的解決方案在技術上是合理的，並能處理所有需求。</p>
        `,
      },
      3: {
        title: "方案反思",
        content: `
          <p>方案反思階段涉及在實施前對提出的方法進行批判性審查和優化。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>批判性審查分析結果和提出的解決方案</li>
            <li>識別潛在差距、邊緣情況或低效問題</li>
            <li>考慮替代方法及其權衡</li>
            <li>根據最佳實踐和設計原則評估解決方案</li>
            <li>根據洞察優化實施策略</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">輸出成果：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>優化後的解決方案設計</li>
            <li>記錄的考慮事項和權衡</li>
            <li>改進的實施策略</li>
          </ul>
          <p class="mt-4">這種反思過程有助於及早發現潛在問題，並確保在投入實施前所選方法是最佳選擇。</p>
        `,
      },
      4: {
        title: "任務分解",
        content: `
          <p>任務分解階段將複雜任務分解為可管理的原子子任務，並建立明確的依賴關係和執行順序。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>將複雜任務分解為更小、可管理的單元</li>
            <li>建立子任務之間的明確依賴關係</li>
            <li>為每個子任務定義範圍和驗收標準</li>
            <li>分配優先級別並評估複雜度</li>
            <li>創建邏輯執行順序</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">支持的更新模式：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li><strong>追加(append)：</strong>保留所有現有任務並添加新任務</li>
            <li><strong>覆蓋(overwrite)：</strong>清除所有未完成的任務並完全替換，同時保留已完成的任務</li>
            <li><strong>選擇性更新(selective)：</strong>根據任務名稱智能匹配更新現有任務，同時保留其他任務</li>
            <li><strong>清除所有任務(clearAllTasks)：</strong>移除所有任務並創建備份</li>
          </ul>
          <p class="mt-4">這種結構化方法通過創建由小型、可實現步驟組成的清晰路線圖，使複雜項目變得可管理。</p>
        `,
      },
      5: {
        title: "任務執行",
        content: `
          <p>任務執行階段涉及按照預定計劃實施特定任務，重點關注質量和需求遵從。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>根據依賴和優先順序選擇要執行的任務</li>
            <li>按照實施指南實施解決方案</li>
            <li>遵循編碼標準和最佳實踐</li>
            <li>處理邊緣情況和錯誤條件</li>
            <li>記錄實施決策和理由</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">執行過程：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>準備必要的資源和環境</li>
            <li>逐步遵循實施指南</li>
            <li>監控進度並處理任何意外問題</li>
            <li>維護代碼質量和文檔</li>
          </ul>
          <p class="mt-4">該階段將計劃轉化為具體結果，實施早期階段設計的解決方案。</p>
        `,
      },
      6: {
        title: "結果驗證",
        content: `
          <p>結果驗證階段確保已實施的任務在標記為完成前滿足所有需求和質量標準。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>驗證是否已實施所有需求</li>
            <li>檢查是否遵循技術標準和最佳實踐</li>
            <li>測試邊緣情況和錯誤處理</li>
            <li>審查代碼質量和文檔</li>
            <li>根據為任務定義的驗證標準進行驗證</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">驗證清單：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>功能正確性：是否按預期工作？</li>
            <li>完整性：是否涵蓋所有需求？</li>
            <li>質量：是否符合編碼標準和最佳實踐？</li>
            <li>性能：是否高效運行？</li>
            <li>文檔：實施是否有良好的文檔？</li>
          </ul>
          <p class="mt-4">這種徹底的驗證過程確保交付高質量的成果，完全滿足需求。</p>
        `,
      },
      7: {
        title: "任務完成",
        content: `
          <p>任務完成階段正式將任務標記為已完成，生成詳細的完成報告，並更新相關依賴任務的狀態。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>成功驗證後正式將任務標記為已完成</li>
            <li>生成全面的完成報告</li>
            <li>更新依賴任務的狀態</li>
            <li>歸檔相關信息以供將來參考</li>
            <li>向利益相關者傳達完成情況</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">完成報告內容：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>已完成工作摘要</li>
            <li>實施亮點和關鍵決策</li>
            <li>遇到的任何值得注意的挑戰及其解決方案</li>
            <li>對未來工作或改進的建議</li>
          </ul>
          <p class="mt-4">完成階段確保任務適當結束，維持工作流程連續性，並為未來項目建立機構知識。</p>
        `,
      },
    },
  };

  // 點擊詳情鏈接打開彈窗
  detailLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const stepIndex = parseInt(this.getAttribute("data-step"));
      const lang = localStorage.getItem("preferred-language") || "en";
      if (stepIndex >= 0 && workflowDetails[lang][stepIndex]) {
        modalTitle.textContent = workflowDetails[lang][stepIndex].title;
        modalContent.innerHTML = workflowDetails[lang][stepIndex].content;
        modal.classList.remove("hidden");
        modal.classList.add("active");
      }
    });
  });

  // 關閉彈窗
  function closeModal() {
    modal.classList.add("hidden");
    modal.classList.remove("active");
  }

  closeBtn.addEventListener("click", closeModal);
  closeBtnAlt.addEventListener("click", closeModal);

  // 點擊彈窗外部關閉
  modal.addEventListener("click", function (e) {
    if (e.target === modal) {
      closeModal();
    }
  });
}

/**
 * 為工作流程時間軸添加連接線動畫
 */
function animateWorkflowConnections() {
  const desktopTimeline = document.querySelector(
    "#workflow .hidden.md\\:block"
  );
  if (!desktopTimeline) return;

  // 當時間軸進入視口時觸發動畫
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const steps = entry.target.querySelectorAll(".workflow-step");

          steps.forEach((step, index) => {
            setTimeout(() => {
              step.classList.add("animated");
            }, index * 200);
          });

          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.3 }
  );

  observer.observe(desktopTimeline);
}

/**
 * 為工作流程步驟圖標添加互動效果
 */
function addWorkflowIconInteractions() {
  const workflowIcons = document.querySelectorAll(
    ".workflow-icon, .workflow-icon-mobile"
  );

  workflowIcons.forEach((icon) => {
    icon.addEventListener("mouseenter", function () {
      const img = this.querySelector("img");
      if (img) {
        img.style.transform = "scale(1.2) rotate(5deg)";
        img.style.transition = "transform 0.3s ease";
      }
    });

    icon.addEventListener("mouseleave", function () {
      const img = this.querySelector("img");
      if (img) {
        img.style.transform = "";
      }
    });

    // 增加點擊效果
    icon.addEventListener("click", function () {
      const link =
        this.parentNode.querySelector(".workflow-detail-link") ||
        this.closest(".flex").querySelector(".workflow-detail-link");

      if (link) {
        link.click();
      }
    });
  });
}

/**
 * 初始化安裝與配置區功能
 */
function initInstallationSection() {
  // 初始化安裝方式選項卡切換
  initInstallTabs();

  // 初始化Cursor IDE配置選項卡切換
  initCursorTabs();

  // 初始化命令行複製按鈕
  initCommandCopyButtons();

  // 添加安裝卡片的動畫效果
  initInstallCardsAnimation();
}

/**
 * 初始化安裝方式選項卡切換
 */
function initInstallTabs() {
  const tabButtons = document.querySelectorAll(".install-tab-btn");
  const contentSections = document.querySelectorAll(".install-content-section");

  if (!tabButtons.length || !contentSections.length) return;

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // 移除所有活動狀態
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      contentSections.forEach((section) => section.classList.add("hidden"));

      // 設置當前活動狀態
      button.classList.add("active");
      const targetId = button.getAttribute("data-target");
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.remove("hidden");
      }
    });
  });
}

/**
 * 初始化Cursor IDE配置選項卡切換
 */
function initCursorTabs() {
  const tabButtons = document.querySelectorAll(".cursor-tab-btn");
  const contentSections = document.querySelectorAll(".cursor-content-section");

  if (!tabButtons.length || !contentSections.length) return;

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // 移除所有活動狀態
      tabButtons.forEach((btn) => btn.classList.remove("active"));
      contentSections.forEach((section) => section.classList.add("hidden"));

      // 設置當前活動狀態
      button.classList.add("active");
      const targetId = button.getAttribute("data-target");
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.classList.remove("hidden");
      }
    });
  });
}

/**
 * 初始化命令行複製按鈕
 */
function initCommandCopyButtons() {
  const copyButtons = document.querySelectorAll(".copy-cmd-btn");

  copyButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const command = button.getAttribute("data-command");
      if (!command) return;

      try {
        await navigator.clipboard.writeText(command);

        // 更新按鈕文字
        const originalText = button.textContent.trim();
        button.textContent = "已複製!";
        button.classList.add("bg-gray-600");
        button.classList.remove(
          "bg-blue-600",
          "bg-green-600",
          "bg-purple-600",
          "hover:bg-blue-700",
          "hover:bg-green-700",
          "hover:bg-purple-700"
        );

        // 恢復原始狀態
        setTimeout(() => {
          button.textContent = originalText;
          button.classList.remove("bg-gray-600");

          // 根據按鈕顏色還原樣式
          if (button.classList.contains("copy-cmd-btn")) {
            if (button.closest("#smithery-install")) {
              button.classList.add("bg-blue-600", "hover:bg-blue-700");
            } else if (button.closest("#manual-install")) {
              button.classList.add("bg-green-600", "hover:bg-green-700");
            } else if (button.closest("#cursor-config")) {
              button.classList.add("bg-purple-600", "hover:bg-purple-700");
            }
          }
        }, 2000);
      } catch (err) {
        console.error("複製命令失敗:", err);
        button.textContent = "複製失敗";
      }
    });
  });
}

/**
 * 安裝卡片的動畫效果
 */
function initInstallCardsAnimation() {
  const installCards = document.querySelectorAll("#installation .grid > div");

  installCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-10px)";
      card.style.boxShadow =
        "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)";

      // 找到卡片內的圖標並添加動畫
      const icon = card.querySelector("svg");
      if (icon) {
        icon.style.transform = "scale(1.2)";
        icon.style.transition = "transform 0.3s ease";
      }
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform = "";
      card.style.boxShadow = "";

      // 恢復圖標
      const icon = card.querySelector("svg");
      if (icon) {
        icon.style.transform = "";
      }
    });
  });
}

/**
 * 初始化頁面滾動到頂部按鈕
 */
function initScrollToTopButton() {
  // 創建回到頂部按鈕元素
  const scrollToTopBtn = document.createElement("button");
  scrollToTopBtn.id = "scrollToTop";
  scrollToTopBtn.innerHTML =
    '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 11l7-7 7 7M5 19l7-7 7 7" /></svg>';
  scrollToTopBtn.className =
    "fixed bottom-5 right-5 bg-blue-600 text-white p-2 rounded-full shadow-lg transform scale-0 transition-transform duration-300";
  scrollToTopBtn.setAttribute("aria-label", "回到頂部");

  // 添加按鈕到文檔
  document.body.appendChild(scrollToTopBtn);

  // 點擊事件 - 平滑滾動到頂部
  scrollToTopBtn.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  // 根據滾動位置顯示或隱藏按鈕
  window.addEventListener("scroll", function () {
    if (window.scrollY > 500) {
      scrollToTopBtn.style.transform = "scale(1)";
    } else {
      scrollToTopBtn.style.transform = "scale(0)";
    }
  });
}

/**
 * 初始化圖片懶加載功能
 */
function initLazyLoading() {
  if ("loading" in HTMLImageElement.prototype) {
    // 瀏覽器支持原生懶加載
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach((img) => {
      img.src = img.dataset.src;
    });
  } else {
    // 回退方案 - 使用 Intersection Observer API
    const imgObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.add("loaded");
          observer.unobserve(img);
        }
      });
    });

    const lazyImages = document.querySelectorAll("img[data-src]");
    lazyImages.forEach((img) => {
      imgObserver.observe(img);
    });
  }
}

/**
 * 初始化頁面進入動畫
 */
function initPageEntranceAnimation() {
  // 頁面加載完成後的動畫效果
  document.body.classList.add("page-loaded");

  // 延遲一點時間後開始序列動畫
  setTimeout(() => {
    const header = document.querySelector("header");
    if (header) {
      header.style.opacity = "1";
      header.style.transform = "translateY(0)";
    }

    const heroContent = document.querySelector("#hero .container");
    if (heroContent) {
      setTimeout(() => {
        heroContent.style.opacity = "1";
        heroContent.style.transform = "translateY(0)";
      }, 200);
    }
  }, 100);
}

/**
 * 為元素添加動畫類
 * @param {Element} element - 要添加動畫的元素
 * @param {string} animationClass - 要添加的動畫類名
 * @param {number} delay - 延遲時間(毫秒)
 */
function addAnimation(element, animationClass, delay = 0) {
  if (!element) return;

  setTimeout(() => {
    element.classList.add(animationClass);

    // 動畫結束後移除類
    element.addEventListener(
      "animationend",
      () => {
        element.classList.remove(animationClass);
      },
      { once: true }
    );
  }, delay);
}

/**
 * 檢測元素是否在視口中
 * @param {Element} element - 要檢測的元素
 * @returns {boolean} - 元素是否在視口中
 */
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.bottom >= 0 &&
    rect.left <= (window.innerWidth || document.documentElement.clientWidth) &&
    rect.right >= 0
  );
}

/**
 * 初始化多語系功能
 */
function initMultiLanguage() {
  // 檢查 i18n.js 是否已載入
  if (typeof i18n !== "undefined") {
    // 優先使用增強版初始化函數
    if (typeof enhancedInitializeLanguage === "function") {
      enhancedInitializeLanguage();
    } else if (typeof initializeLanguage === "function") {
      // 兼容性處理，如果增強版函數不存在則使用原始方法
      initializeLanguage();
    } else {
      console.warn("多語系初始化函數不可用，將使用基本初始化");
      // 基本初始化 - 在i18n.js無法正確載入時提供基本功能
      try {
        const currentLang =
          localStorage.getItem("preferred-language") ||
          (navigator.language && navigator.language.startsWith("zh")
            ? "zh-TW"
            : "en");
        document.documentElement.setAttribute("lang", currentLang);
      } catch (e) {
        console.error("基本語言初始化失敗:", e);
      }
    }

    // 為語言切換添加自定義事件
    try {
      document.querySelectorAll(".lang-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
          const lang = this.getAttribute("data-lang");

          // 優先使用增強版語言切換函數
          if (typeof enhancedSetLanguage === "function") {
            enhancedSetLanguage(lang);
          } else if (typeof setLanguageWithAnimation === "function") {
            // 次優先使用帶動畫效果的語言切換
            setLanguageWithAnimation(lang);
          } else if (typeof setLanguage === "function") {
            // 兼容性處理，使用基本語言切換函數
            setLanguage(lang);
          } else {
            console.warn("語言切換函數不可用");
            // 最基本處理 - 更新 HTML lang 屬性並保存偏好
            try {
              localStorage.setItem("preferred-language", lang);
              document.documentElement.setAttribute("lang", lang);
            } catch (e) {
              console.error("基本語言切換失敗:", e);
            }
          }
        });
      });
    } catch (e) {
      console.error("為語言按鈕添加事件監聽器時出錯:", e);
    }

    // 初始化時執行批量翻譯，優化性能
    if (typeof batchApplyTranslations === "function") {
      batchApplyTranslations();
    }
  } else {
    console.warn("i18n.js 尚未載入，無法啟用完整多語系功能");
    // 嘗試提供基本的多語系支持
    try {
      const basicLanguageSupport = function () {
        const langBtns = document.querySelectorAll(".lang-btn");
        if (langBtns.length === 0) return;

        langBtns.forEach((btn) => {
          btn.addEventListener("click", function () {
            const lang = this.getAttribute("data-lang");
            try {
              localStorage.setItem("preferred-language", lang);
              document.documentElement.setAttribute("lang", lang);

              // 更新按鈕狀態
              langBtns.forEach((b) => {
                if (b.getAttribute("data-lang") === lang) {
                  b.classList.add("active");
                } else {
                  b.classList.remove("active");
                }
              });
            } catch (e) {
              console.error("基本語言切換失敗:", e);
            }
          });
        });

        // 初始化按鈕狀態
        try {
          const savedLang =
            localStorage.getItem("preferred-language") ||
            (navigator.language && navigator.language.startsWith("zh")
              ? "zh-TW"
              : "en");

          langBtns.forEach((btn) => {
            if (btn.getAttribute("data-lang") === savedLang) {
              btn.classList.add("active");
            } else {
              btn.classList.remove("active");
            }
          });

          document.documentElement.setAttribute("lang", savedLang);
        } catch (e) {
          console.error("初始化語言按鈕狀態失敗:", e);
        }
      };

      basicLanguageSupport();
    } catch (e) {
      console.error("基本多語系支持初始化失敗:", e);
    }
  }

  // 監聽語言切換事件
  try {
    document.addEventListener("languageChanged", function (event) {
      const lang = event.detail.language;
      console.log("Language changed to:", lang);

      // 使用 translateText 函數更新特殊元素
      const updateSpecialElements = function () {
        // 安全地取得翻譯函數
        const getTranslation = (key, defaultText) => {
          if (typeof safeTranslate === "function") {
            return safeTranslate(key, defaultText);
          } else if (typeof translateText === "function") {
            return translateText(key, defaultText);
          } else {
            return lang === "en" ? defaultText.en : defaultText.zh;
          }
        };

        try {
          // 更新複製按鈕文字
          const copyBtns = document.querySelectorAll(".copy-cmd-btn");
          const copyText = getTranslation("common.copy", {
            en: "Copy",
            zh: "複製",
          });

          copyBtns.forEach((btn) => {
            // 只更新沒有顯示"已複製"的按鈕
            if (
              btn.textContent !== "Copied!" &&
              btn.textContent !== "已複製!"
            ) {
              btn.textContent = copyText;
            }
          });
        } catch (e) {
          console.warn("更新複製按鈕文字失敗:", e);
        }

        try {
          // 更新模態窗口中的關閉按鈕文字
          const closeModalBtn = document.getElementById("close-modal-btn");
          if (closeModalBtn) {
            closeModalBtn.textContent = getTranslation("common.close", {
              en: "Close",
              zh: "關閉",
            });
          }
        } catch (e) {
          console.warn("更新關閉按鈕文字失敗:", e);
        }
      };

      // 使用 setTimeout 避免阻塞 UI
      setTimeout(updateSpecialElements, 0);

      // 根據當前語言更新工作流程模態內容
      try {
        updateWorkflowModalContent(lang);
      } catch (e) {
        console.warn("更新工作流程模態內容失敗:", e);
      }
    });
  } catch (e) {
    console.error("添加語言變更事件監聽器失敗:", e);
  }
}

/**
 * 根據當前語言更新工作流程模態窗口內容
 * @param {string} lang - 當前語言代碼 ("en" 或 "zh-TW")
 */
function updateWorkflowModalContent(lang) {
  const modal = document.getElementById("workflow-detail-modal");
  if (!modal) return;

  // 獲取當前顯示的步驟
  const modalTitle = document.getElementById("modal-title");
  const modalContent = document.getElementById("modal-content");
  const currentStep = modal.getAttribute("data-current-step");

  if (currentStep && modalTitle && modalContent) {
    // 從工作流程詳情中獲取對應語言的內容
    const workflowDetails = getWorkflowDetails();
    const langKey = lang === "en" ? "en" : "zh-TW";

    if (workflowDetails[langKey] && workflowDetails[langKey][currentStep]) {
      const stepData = workflowDetails[langKey][currentStep];

      // 使用 requestAnimationFrame 優化渲染性能
      requestAnimationFrame(function () {
        modalTitle.textContent = stepData.title;
        modalContent.innerHTML = stepData.content;

        // 為動態生成的內容添加 data-i18n 屬性
        const dynamicElements = modalContent.querySelectorAll("h4, p, li");
        dynamicElements.forEach(function (el, index) {
          const key = `workflow.step${currentStep}.content.${index}`;
          el.setAttribute("data-i18n-dynamic", key);
        });
      });
    }
  }
}

/**
 * 獲取工作流程詳情數據
 * @returns {Object} 工作流程詳情對象
 */
function getWorkflowDetails() {
  // 返回工作流程詳情數據
  return {
    // 現有數據保持不變
    en: {
      1: {
        title: "Task Planning",
        content: `
          <p>The task planning stage is the initial phase where AI assistants define project scope, set goals, and establish success criteria.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Clarify project requirements and constraints</li>
            <li>Set clear objectives and define measurable success criteria</li>
            <li>Establish project boundaries and identify stakeholders</li>
            <li>Create a high-level plan with timeline estimates</li>
            <li>Optionally reference existing tasks for continuous planning</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Outputs:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Comprehensive task description</li>
            <li>Clear success criteria</li>
            <li>Technical requirements and constraints</li>
          </ul>
          <p class="mt-4">This stage lays the foundation for all subsequent work, ensuring that both the AI assistant and the user have a shared understanding of what needs to be accomplished.</p>
        `,
      },
      2: {
        title: "In-depth Analysis",
        content: `
          <p>The in-depth analysis stage involves a thorough examination of the requirements and technical landscape to develop a viable implementation strategy.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Analyze requirements and identify technical challenges</li>
            <li>Evaluate technical feasibility and potential risks</li>
            <li>Research best practices and available solutions</li>
            <li>Systematically review existing codebase if applicable</li>
            <li>Develop initial implementation concepts</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Outputs:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Technical feasibility assessment</li>
            <li>Risk identification and mitigation strategies</li>
            <li>Initial implementation approach</li>
            <li>Pseudocode or architectural diagrams where appropriate</li>
          </ul>
          <p class="mt-4">This stage ensures that the proposed solution is technically sound and addresses all requirements before proceeding to implementation.</p>
        `,
      },
      3: {
        title: "Solution Reflection",
        content: `
          <p>The solution reflection stage involves critical review and optimization of the proposed approach before implementation.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Critically review the analysis results and proposed solutions</li>
            <li>Identify potential gaps, edge cases, or inefficiencies</li>
            <li>Consider alternative approaches and their trade-offs</li>
            <li>Evaluate solution against best practices and design principles</li>
            <li>Refine implementation strategy based on insights</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Outputs:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Optimized solution design</li>
            <li>Documented considerations and trade-offs</li>
            <li>Refined implementation strategy</li>
          </ul>
          <p class="mt-4">This reflective process helps catch potential issues early and ensures the chosen approach is optimal before investing in implementation.</p>
        `,
      },
      4: {
        title: "Task Decomposition",
        content: `
          <p>The task decomposition stage breaks down complex tasks into manageable, atomic subtasks with clear dependencies and execution order.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Break down complex tasks into smaller, manageable units</li>
            <li>Establish clear dependencies between subtasks</li>
            <li>Define scope and acceptance criteria for each subtask</li>
            <li>Assign priority levels and estimate complexity</li>
            <li>Create a logical execution sequence</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Supported Update Modes:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li><strong>Append:</strong> Keep all existing tasks and add new ones</li>
            <li><strong>Overwrite:</strong> Clear all uncompleted tasks and completely replace them, while preserving completed tasks</li>
            <li><strong>Selective:</strong> Intelligently update existing tasks based on task names, preserving tasks not in the list</li>
            <li><strong>Clear All Tasks:</strong> Remove all tasks and create a backup</li>
          </ul>
          <p class="mt-4">This structured approach makes complex projects manageable by creating a clear roadmap of small, achievable steps.</p>
        `,
      },
      5: {
        title: "Task Execution",
        content: `
          <p>The task execution stage involves implementing specific tasks according to the predetermined plan, with a focus on quality and adherence to requirements.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Select tasks for execution based on dependencies and priorities</li>
            <li>Implement solutions following the implementation guide</li>
            <li>Follow coding standards and best practices</li>
            <li>Handle edge cases and error conditions</li>
            <li>Document implementation decisions and rationale</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Execution Process:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Prepare necessary resources and environment</li>
            <li>Follow the implementation guide step by step</li>
            <li>Monitor progress and handle any unexpected issues</li>
            <li>Maintain code quality and documentation</li>
          </ul>
          <p class="mt-4">This stage transforms plans into concrete results, implementing the solutions designed in earlier stages.</p>
        `,
      },
      6: {
        title: "Result Verification",
        content: `
          <p>The result verification stage ensures that implemented tasks meet all requirements and quality standards before being marked as complete.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Verify that all requirements have been implemented</li>
            <li>Check for adherence to technical standards and best practices</li>
            <li>Test edge cases and error handling</li>
            <li>Review code quality and documentation</li>
            <li>Validate against the verification criteria defined for the task</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Verification Checklist:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Functional correctness: Does it work as expected?</li>
            <li>Completeness: Are all requirements addressed?</li>
            <li>Quality: Does it meet coding standards and best practices?</li>
            <li>Performance: Does it operate efficiently?</li>
            <li>Documentation: Is the implementation well-documented?</li>
          </ul>
          <p class="mt-4">This thorough verification process ensures high-quality deliverables that fully satisfy requirements.</p>
        `,
      },
      7: {
        title: "Task Completion",
        content: `
          <p>The task completion stage formally marks tasks as complete, generates detailed completion reports, and updates the status of dependent tasks.</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Formally mark task as completed after successful verification</li>
            <li>Generate a comprehensive completion report</li>
            <li>Update the status of dependent tasks</li>
            <li>Archive relevant information for future reference</li>
            <li>Communicate completion to stakeholders</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Completion Report Contents:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Summary of completed work</li>
            <li>Implementation highlights and key decisions</li>
            <li>Any notable challenges encountered and their solutions</li>
            <li>Recommendations for future work or improvements</li>
          </ul>
          <p class="mt-4">The completion stage ensures proper closure of tasks, maintains workflow continuity, and builds institutional knowledge for future projects.</p>
        `,
      },
    },
    "zh-TW": {
      1: {
        title: "任務規劃",
        content: `
          <p>任務規劃階段是初始階段，AI助手定義項目範圍、設定目標，並建立成功標準。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>釐清項目需求和約束條件</li>
            <li>設定明確目標和定義可衡量的成功標準</li>
            <li>確立項目界限和識別相關利益方</li>
            <li>創建高級計劃及時間估算</li>
            <li>可選擇參考現有任務進行持續規劃</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">輸出成果：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>全面的任務描述</li>
            <li>明確的成功標準</li>
            <li>技術需求和約束條件</li>
          </ul>
          <p class="mt-4">此階段為所有後續工作奠定基礎，確保AI助手和用戶對需要完成的工作有共同理解。</p>
        `,
      },
      2: {
        title: "深入分析",
        content: `
          <p>深入分析階段涉及對需求和技術環境的徹底檢查，以制定可行的實施策略。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>分析需求並識別技術挑戰</li>
            <li>評估技術可行性和潛在風險</li>
            <li>研究最佳實踐和可用解決方案</li>
            <li>系統性地審查現有代碼庫（如適用）</li>
            <li>開發初步實施概念</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">輸出成果：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>技術可行性評估</li>
            <li>風險識別和緩解策略</li>
            <li>初步實施方法</li>
            <li>適當的偽代碼或架構圖</li>
          </ul>
          <p class="mt-4">此階段確保在進行實施前，提出的解決方案在技術上是合理的，並能處理所有需求。</p>
        `,
      },
      3: {
        title: "方案反思",
        content: `
          <p>方案反思階段涉及在實施前對提出的方法進行批判性審查和優化。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>批判性審查分析結果和提出的解決方案</li>
            <li>識別潛在差距、邊緣情況或低效問題</li>
            <li>考慮替代方法及其權衡</li>
            <li>根據最佳實踐和設計原則評估解決方案</li>
            <li>根據洞察優化實施策略</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">輸出成果：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>優化後的解決方案設計</li>
            <li>記錄的考慮事項和權衡</li>
            <li>改進的實施策略</li>
          </ul>
          <p class="mt-4">這種反思過程有助於及早發現潛在問題，並確保在投入實施前所選方法是最佳選擇。</p>
        `,
      },
      4: {
        title: "任務分解",
        content: `
          <p>任務分解階段將複雜任務分解為可管理的原子子任務，並建立明確的依賴關係和執行順序。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>將複雜任務分解為更小、可管理的單元</li>
            <li>建立子任務之間的明確依賴關係</li>
            <li>為每個子任務定義範圍和驗收標準</li>
            <li>分配優先級別並評估複雜度</li>
            <li>創建邏輯執行順序</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">支持的更新模式：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li><strong>追加(append)：</strong>保留所有現有任務並添加新任務</li>
            <li><strong>覆蓋(overwrite)：</strong>清除所有未完成的任務並完全替換，同時保留已完成的任務</li>
            <li><strong>選擇性更新(selective)：</strong>根據任務名稱智能匹配更新現有任務，同時保留其他任務</li>
            <li><strong>清除所有任務(clearAllTasks)：</strong>移除所有任務並創建備份</li>
          </ul>
          <p class="mt-4">這種結構化方法通過創建由小型、可實現步驟組成的清晰路線圖，使複雜項目變得可管理。</p>
        `,
      },
      5: {
        title: "任務執行",
        content: `
          <p>任務執行階段涉及按照預定計劃實施特定任務，重點關注質量和需求遵從。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">主要活動：</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>根據依賴和優先順序選擇要執行的任務</li>
            <li>按照實施指南實施解決方案</li>
            <li>遵循編碼標準和最佳實踐</li>
            <li>處理邊緣情況和錯誤條件</li>
            <li>記錄實施決策和理由</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Execution Process:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Prepare necessary resources and environment</li>
            <li>Follow the implementation guide step by step</li>
            <li>Monitor progress and handle any unexpected issues</li>
            <li>Maintain code quality and documentation</li>
          </ul>
          <p class="mt-4">This stage transforms plans into concrete results, implementing the solutions designed in earlier stages.</p>
        `,
      },
      6: {
        title: "結果驗證",
        content: `
          <p>結果驗證階段確保已實施的任務在標記為完成前滿足所有需求和質量標準。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Verify that all requirements have been implemented</li>
            <li>Check for adherence to technical standards and best practices</li>
            <li>Test edge cases and error handling</li>
            <li>Review code quality and documentation</li>
            <li>Validate against the verification criteria defined for the task</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Verification Checklist:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Functional correctness: Does it work as expected?</li>
            <li>Completeness: Are all requirements addressed?</li>
            <li>Quality: Does it meet coding standards and best practices?</li>
            <li>Performance: Does it operate efficiently?</li>
            <li>Documentation: Is the implementation well-documented?</li>
          </ul>
          <p class="mt-4">This thorough verification process ensures high-quality deliverables that fully satisfy requirements.</p>
        `,
      },
      7: {
        title: "任務完成",
        content: `
          <p>任務完成階段正式將任務標記為已完成，生成詳細的完成報告，並更新相關依賴任務的狀態。</p>
          <h4 class="text-lg font-semibold mt-4 mb-2">Key Activities:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>成功驗證後正式將任務標記為已完成</li>
            <li>生成全面的完成報告</li>
            <li>更新依賴任務的狀態</li>
            <li>歸檔相關信息以供將來參考</li>
            <li>向利益相關者傳達完成情況</li>
          </ul>
          <h4 class="text-lg font-semibold mt-4 mb-2">Completion Report Contents:</h4>
          <ul class="list-disc pl-6 space-y-2">
            <li>Summary of completed work</li>
            <li>Implementation highlights and key decisions</li>
            <li>Any notable challenges encountered and their solutions</li>
            <li>Recommendations for future work or improvements</li>
          </ul>
          <p class="mt-4">The completion stage ensures proper closure of tasks, maintains workflow continuity, and builds institutional knowledge for future projects.</p>
        `,
      },
    },
  };
}
