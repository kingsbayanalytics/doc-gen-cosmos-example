# 開發守則

本文檔為 AI Agent 在 `mcp-shrimp-task-manager` 專案中執行開發任務的專用規範。

## 1. 專案概述

- **專案名稱**: `mcp-shrimp-task-manager`
- **目的**: 一個為 AI Agents 設計的任務管理工具，強調思維鏈、反思和風格一致性。它將自然語言轉換為結構化的開發任務，並具有依賴追蹤和迭代優化功能。
- **技術棧**:
  - 主要語言: TypeScript
  - 執行環境: Node.js (ES Module)
  - 主要框架/函式庫: Express.js (用於可能的 API 或 WebGUI), Zod (用於資料驗證)
  - 套件管理器: npm
- **核心功能**:
  - 自然語言任務解析
  - 結構化任務生成與管理
  - 任務依賴關係追蹤
  - 任務執行與驗證輔助
  - 與 AI Agent 的思維流程整合

## 2. 專案架構

- **主要原始碼目錄**: `src/`
  - `src/index.ts`: 主要應用程式入口或模組匯出點。**修改此檔案需謹慎評估影響範圍。**
  - `src/utils/`: 通用工具函式。
  - `src/types/`: TypeScript 型別定義。**新增或修改型別時，務必確保與 Zod schema (如適用) 一致性。**
  - `src/tools/`: 專案特定工具或與外部服務整合的模組。
  - `src/models/`: 資料模型定義 (可能與 Zod schemas 相關)。
  - `src/prompts/`: AI 互動相關的提示詞模板。**修改或新增提示詞時，需考慮對 AI Agent 行為的潛在影響。**
  - `src/public/`: WebGUI 或其他靜態資源。
  - `src/tests/`: 單元測試和整合測試。
- **編譯輸出目錄**: `dist/` (此目錄由 `tsc` 自動生成，**禁止手動修改此目錄內容**)。
- **設定檔**:
  - `package.json`: 專案依賴和腳本。**新增依賴後，必須執行 `npm install`。**
  - `tsconfig.json`: TypeScript 編譯設定。**非必要情況下，禁止修改 `"strict": true` 設定。**
  - `.env.example` & `.env`: 環境變數設定。**敏感資訊不得提交至版本控制。**
- **文件**:
  - `README.md`: 主要專案說明文件。
  - `docs/`: 可能包含更詳細的架構、API 文件等。
  - `CHANGELOG.md`: 版本變更紀錄。**每次發布新版本前必須更新。**
  - `data/WebGUI.md`: 包含 Task Manager UI 的連結。

## 3. 程式碼規範

### 3.1. 命名規範

- **變數與函式**: 使用小駝峰命名法 (camelCase)。
  - _範例 (可做)_: `const taskName = "example"; function processTask() {}`
  - _範例 (不可做)_: `const Task_Name = "example"; function Process_Task() {}`
- **類別與介面**: 使用大駝峰命名法 (PascalCase)。
  - _範例 (可做)_: `class TaskManager {}; interface ITaskOptions {}`
  - _範例 (不可做)_: `class taskManager {}; interface iTaskOptions {}`
- **檔案名稱**: 使用小駝峰命名法或橫線連接 (kebab-case) 的 `.ts` 檔案。
  - _範例 (可做)_: `taskProcessor.ts`, `task-utils.ts`
  - _範例 (不可做)_: `TaskProcessor.ts`, `task_utils.ts`
- **常數**: 使用全大寫蛇形命名法 (UPPER_SNAKE_CASE)。
  - _範例 (可做)_: `const MAX_RETRIES = 3;`
  - _範例 (不可做)_: `const maxRetries = 3;`

### 3.2. 格式要求

- **縮排**: 使用 2 個空格進行縮排。**禁止使用 Tab 字元。**
- **分號**: 每行敘述句尾必須加上分號。
- **引號**: 字串優先使用單引號 (`'`)，除非字串本身包含單引號。
  - _範例 (可做)_: `const message = 'Hello World'; const complex = "It\\'s complex";`
  - _範例 (不可做)_: `const message = "Hello World";`
- **最大行長度**: 建議不超過 120 字元。
- **註解**:
  - 單行註解使用 `//`。
  - 多行註解使用 `/* ... */`。
  - JSDoc 風格的註解應用於公開的函式、類別和方法。
    - _範例 (可做)_:
      ```typescript
      /**
       * Processes a given task.
       * @param taskId The ID of the task to process.
       * @returns True if successful, false otherwise.
       */
      function processTaskById(taskId: string): boolean {
        // implementation
        return true;
      }
      ```

### 3.3. TypeScript 特定規範

- **型別註解**: 所有函式參數、回傳值和變數宣告都應有明確的型別註解。**禁止使用 `any` 型別，除非在極特殊且無法避免的情況下，並需加上註解說明原因。**
  - _範例 (可做)_: `function greet(name: string): string { return \`Hello, ${name}\`; }`
  - _範例 (不可做)_: `function greet(name): any { return "Hello, " + name; }`
- **介面與型別別名**: 優先使用介面 (Interface) 定義物件的形狀，使用型別別名 (Type Alias) 定義聯合型別、元組或其他複雜型別。
- **ES Module**: 使用 `import` 和 `export` 語法。
  - _範例 (可做)_: `import { Task } from './models/task'; export class TaskService {}`
  - _範例 (不可做)_: `const Task = require('./models/task'); module.exports = TaskService;`
- **嚴格模式**: 專案已啟用 `"strict": true`。必須解決所有 TypeScript 的嚴格模式錯誤。

## 4. 功能實作規範

### 4.1. 通用原則

- **單一職責原則 (SRP)**: 每個函式和類別應只負責一項功能。
- **保持簡潔 (KISS)**: 避免過度複雜的解決方案。
- **重複利用**: 盡可能將通用邏輯抽取為可重用函式或類別，存放於 `src/utils/` 或相關模組。
- **錯誤處理**:
  - 使用 `try...catch` 處理預期內的錯誤。
  - 對於關鍵操作，應提供清晰的錯誤訊息。
  - 考慮使用自定義錯誤類別以提供更豐富的錯誤資訊。
- **日誌記錄**:
  - 在關鍵操作、錯誤處理和重要狀態變更時加入日誌記錄。
  - 考慮使用結構化日誌。
  - **禁止在日誌中記錄敏感資訊 (如密碼、API Keys)。**

### 4.2. Zod 使用

- 位於 `src/models/` 或 `src/types/` 的資料結構定義，應優先使用 Zod schema 進行定義和驗證。
- Zod schema 應與 TypeScript 型別保持同步。可使用 `z.infer<typeof schema>` 生成型別。

  - _範例 (可做)_:

    ```typescript
    import { z } from "zod";

    export const TaskSchema = z.object({
      id: z.string().uuid(),
      name: z.string().min(1),
      description: z.string().optional(),
    });

    export type Task = z.infer<typeof TaskSchema>;
    ```

### 4.3. Express.js 使用 (若有 API/WebGUI)

- 路由定義應清晰且遵循 RESTful 原則 (若為 API)。
- 中介軟體 (Middleware) 應有效組織，例如錯誤處理中介軟體、日誌中介軟體等。
- 所有外部輸入 (request parameters, body, query) **必須**經過 Zod 或類似機制驗證。

## 5. 框架/外掛程式/第三方庫使用規範

- **新增依賴**:
  - **必須**先評估依賴的必要性、維護狀態和安全性。
  - 使用 `npm install <package-name>` (用於執行依賴) 或 `npm install --save-dev <package-name>` (用於開發依賴)。
  - **必須**在 `package.json` 中指定明確的版本範圍 (例如 `^1.2.3` 或 `~1.2.3`)，避免使用 `*`。
- **更新依賴**: 定期檢查並更新依賴至最新穩定版本，以獲取安全性修補和新功能。更新前需評估潛在的破壞性變更。
- **移除依賴**: 若不再需要某個依賴，使用 `npm uninstall <package-name>` 將其移除，並從程式碼中移除相關引用。

## 6. 工作流程規範

### 6.1. 開發流程

1.  **理解任務**: 仔細閱讀任務描述、需求和驗收標準。
2.  **分支管理**: 從最新的 `main` (或 `develop`) 分支建立新的特性分支 (feature branch)。分支名稱應簡潔明瞭，例如 `feature/add-task-editing` 或 `fix/login-bug`。
3.  **編碼與測試**:
    - 按照本規範進行編碼。
    - **必須**為新功能或修復的 bug 編寫單元測試 (存放於 `src/tests/`)。
    - 執行 `npm run build` 確保程式碼可以成功編譯。
    - 本地執行 `npm run dev` 或 `npm run start` 進行測試。
4.  **程式碼提交**:
    - Git commit message 應遵循 Conventional Commits 規範 (例如 `feat: add user authentication`, `fix: resolve issue with task sorting`)。
    - **禁止提交包含 `console.log` 或其他偵錯訊息的程式碼至主要分支。**
5.  **Pull Request (PR)**:
    - 將特性分支推送到遠端倉庫，並建立 Pull Request 至 `main` (或 `develop`) 分支。
    - PR 描述應清晰說明變更內容和原因。
6.  **Code Review**: 等待其他開發者或 AI Agent 進行 Code Review。
7.  **合併與部署**: Code Review 通過後，合併 PR。部署流程依專案設定。

### 6.2. 版本控制 (Git)

- **主要分支**:
  - `main`: 代表穩定且可部署的產品版本。
  - `develop` (若使用): 代表開發中的最新版本。
- **提交頻率**: 建議小步快跑，頻繁提交有意義的變更。
- **解決衝突**: 合併或 rebase 分支時，若發生衝突，**必須**仔細解決，確保程式碼的正確性和完整性。

### 6.3. CHANGELOG 更新

- 在發布新版本之前，**必須**更新 `CHANGELOG.md`。
- 紀錄應包含版本號、發布日期以及新增功能、修復的錯誤和重大變更列表。

## 7. 關鍵檔案交互規範

- **修改 `src/types/` 或 `src/models/` (特別是 Zod schemas)**:
  - **必須**檢查並更新所有引用到這些型別或 schema 的檔案，確保型別一致性。
  - **必須**重新執行相關測試。
- **修改 `src/index.ts`**:
  - 若修改了模組的匯出 API，**必須**檢查所有依賴此模組的專案或檔案，並進行相應調整。
- **修改 `package.json` (特別是 `dependencies` 或 `scripts`)**:
  - **必須**通知團隊成員或相關 AI Agent 執行 `npm install`。
  - 若修改 `scripts`，需確保 CI/CD 流程 (若有) 也相應更新。
- **修改 `.env.example`**:
  - **必須**同步更新所有開發環境的 `.env` 檔案，並通知團隊成員。
- **修改 `README.md` 或 `docs/` 內的文檔**:
  - 若變更涉及核心功能或使用方式，**必須**確保文件內容的準確性和即時性。

## 8. AI 決策規範

### 8.1. 處理模糊請求

- 當收到模糊的開發指令時 (例如 "優化任務列表顯示")：
  1.  **嘗試澄清**: 若可能，向用戶或任務發起者請求更具體的細節或預期結果。
  2.  **分析上下文**: 檢查相關程式碼 (`src/`)、現有 UI (若有)、相關 issue (若有) 來推斷可能的意圖。
  3.  **提出方案**: 基於分析，提出 1-2 個具體的實施方案，並說明各自的優缺點及預計工作量。
  4.  **等待確認**: 在獲得明確指示前，不進行大規模程式碼修改。

### 8.2. 錯誤/異常處理策略

- **優先級**:
  1.  **使用者體驗**: 避免程式崩潰，提供友好的錯誤提示。
  2.  **資料完整性**: 確保錯誤不會導致資料損壞或不一致。
  3.  **系統穩定性**: 記錄詳細錯誤資訊以供排查。
- **選擇**:
  - 對於可預期的錯誤 (例如使用者輸入無效)，應在該操作的上下文中處理並給予提示。
  - 對於意外的系統錯誤，應捕獲、記錄，並可能向上拋出或觸發全域錯誤處理機制。

### 8.3. 依賴選擇

- 當需要引入新的第三方函式庫時：
  1.  **檢查現有**: 確認專案中是否已有可滿足需求的類似函式庫。
  2.  **評估選項**:
      - **活躍度與社群支援**: 選擇維護良好、社群活躍的函式庫。
      - **輕量級**: 避免引入過於龐大或功能冗餘的函式庫。
      - **安全性**: 檢查是否有已知的安全漏洞。
      - **授權條款 (License)**: 確保與專案授權相容。
  3.  **最小化原則**: 僅引入確實需要的函式庫。

## 9. 禁止事項

- **禁止直接修改 `dist/` 目錄下的任何檔案。** 該目錄為編譯產物。
- **禁止在未執行 `npm install` 的情況下，假定新依賴可用。**
- **禁止在主要分支 (`main` 或 `develop`) 直接提交未經測試或未完成的程式碼。** 必須使用特性分支。
- **禁止提交包含 API Keys、密碼或其他敏感資訊的程式碼至版本控制系統。** 使用 `.env` 檔案管理此類資訊。
- **禁止在未告知或未獲同意的情況下，大幅修改核心架構或公共 API。**
- **禁止忽略 TypeScript 的型別錯誤。** 必須解決所有 `tsc` 報告的錯誤。
- **禁止在沒有充分理由和註解的情況下使用 `any` 型別。**
- **禁止在程式碼中留下大量的 `console.log` 或其他臨時偵錯程式碼。**
- **禁止在未更新 `CHANGELOG.md` 的情況下發布新版本。**
- **禁止引入與專案 MIT 授權條款不相容的第三方函式庫。**

## 10. 更新此規範文件 (`shrimp-rules.md`)

- 當專案的技術棧、核心架構、主要工作流程或重要規範發生變動時，**必須**同步更新此文件。
- 更新請求應明確指出需要變更的章節和內容。
- 若收到模糊的 "更新規則" 指令，AI Agent **必須**：
  1.  自主分析當前程式碼庫的變更 (例如 `git diff`、最近的 commit)。
  2.  比較現有的 `shrimp-rules.md` 與專案現狀，找出不一致或過時的規則。
  3.  在 `process_thought` 階段列出推斷的更新點及其理由。
  4.  提出具體的修改建議，或直接編輯此文件。
  5.  **嚴格禁止**在執行自主分析前就模糊請求向用戶尋求澄清。

---

此開發守則旨在確保 AI Agent 能夠高效、一致且安全地參與 `mcp-shrimp-task-manager` 專案的開發。
