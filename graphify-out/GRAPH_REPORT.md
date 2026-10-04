# Graph Report - claude code setup  (2026-06-27)

## Corpus Check
- 80 files · ~136,523 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 933 nodes · 1286 edges · 54 communities (48 shown, 6 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 92 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]

## God Nodes (most connected - your core abstractions)
1. `TestLiteLLMProvider` - 36 edges
2. `TestVideoService` - 31 edges
3. `TestVoiceService` - 26 edges
4. `VideoParams` - 19 edges
5. `MaterialInfo` - 16 edges
6. `tts()` - 16 edges
7. `TestSocialMetadata` - 16 edges
8. `TestCli` - 15 edges
9. `TaskManager` - 14 edges
10. `VideoAspect` - 13 edges

## Surprising Connections (you probably didn't know these)
- `TestVideoService` --uses--> `TaskQueueFullError`  [INFERRED]
  MoneyPrinterTurbo/test/services/test_video.py → MoneyPrinterTurbo/app/controllers/manager/base_manager.py
- `RedisTaskManager` --uses--> `TaskManager`  [INFERRED]
  MoneyPrinterTurbo/app/controllers/manager/redis_manager.py → MoneyPrinterTurbo/app/controllers/manager/base_manager.py
- `TestVideoService` --uses--> `InMemoryTaskManager`  [INFERRED]
  MoneyPrinterTurbo/test/services/test_video.py → MoneyPrinterTurbo/app/controllers/manager/memory_manager.py
- `start()` --calls--> `VideoConcatMode`  [INFERRED]
  MoneyPrinterTurbo/app/services/task.py → MoneyPrinterTurbo/app/models/schema.py
- `SubClippedVideoClip` --uses--> `VideoAspect`  [INFERRED]
  MoneyPrinterTurbo/app/services/video.py → MoneyPrinterTurbo/app/models/schema.py

## Import Cycles
- None detected.

## Communities (54 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (62): exception_handler(), get_application(), Application implementation - ASGI., Initialize FastAPI application.      Returns:        FastAPI: Application obj, validation_exception_handler(), Application configuration - root APIRouter.  Defines all FastAPI application e, BackgroundTasks, BaseModel (+54 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (70): Communicate, azure_tts_v1(), azure_tts_v2(), _build_subtitle_formatter(), _build_subtitle_items_from_edge_cues(), _build_subtitle_items_from_legacy_submaker(), _configure_pydub_ffmpeg(), convert_rate_to_percent() (+62 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (17): 验证 LiteLLM provider 的主路径不依赖真实网络和私有 API key。          这里用 fake module 注入 `sys.m, 某些 OpenAI-compatible 网关在内容过滤或安全拦截时会返回         HTTP 200，但 `choices[0].message` 为, 自定义 OpenAI-compatible base_url 可能包含代理网关的 user:pass。         SDK 抛错时常会把 URL 带回异常, DashScope chat 模式会把文本放在 `output.choices[0].message.content`。         这里覆盖 issue, 保留旧 DashScope completion 响应结构的兼容路径。, Qwen 空响应应返回可诊断错误，而不是底层 AttributeError。, Qwen chat 响应 choices 为空时应返回明确错误。, AIHubMix 是 OpenAI-compatible 网关。这里用 fake OpenAI client         验证独立 provider 会使 (+9 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (45): Enum, ImageClip, VideoConcatMode, VideoTransitionMode, close_clip(), combine_videos(), concat_video_clips_with_ffmpeg(), delete_files() (+37 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (17): {       "video_subject": "A day in Shanghai",       "video_script": "",, VideoSocialMetadataParams, VideoSocialMetadataRequest, 按文案顺序匹配素材依赖 LLM 返回有序关键词。这里不调用真实模型，         只验证服务层会把“按脚本叙事顺序输出”的约束写入 prompt，避免, API 请求模型需要限制高级 prompt 参数，避免外部调用绕过 WebUI         传入异常段落数或超长提示词，导致模型成本和结果不可控。, reasoning 模型可能返回 `<think>...</think>`。脚本生成链路必须只保留         最终正文，避免思考过程进入字幕和配音。, 如果模型只返回思考块而没有最终答案，应视为空内容，触发重试或明确错误。, 某些网关可能因为截断只返回未闭合的 `<think>`。这种内容同样不能         进入最终脚本；如果清理后没有正文，就应该按空响应处理。 (+9 more)

### Community 5 - "Community 5"
Cohesion: 0.04
Nodes (22): BGM 列表接口现在只暴露文件名；生成视频时应能把文件名安全解析回         resource/songs 白名单目录，保持正常使用路径可用。, 用户在 WebUI 中可能直接填写 ./resource/songs/xxx.mp3。该路径虽然是         项目根目录相对路径，但实际文件仍在 res, 用户传入的 bgm_file 不能直接作为本地路径打开，否则可能读取系统文件。         即使外部文件存在，也必须因为不在 songs 目录内被拒绝。, 配置中显式指定 ffmpeg 时，应优先使用该路径。, Windows 便携包里系统 PATH 可能没有 ffmpeg，但 moviepy 依赖的         imageio-ffmpeg 通常会提供可执行文件, 用户选择的硬件编码器必须先经过 FFmpeg encoder 列表检测。检测不到         时直接回退 libx264，避免生成任务在写文件阶段才失败。, Windows 上用户配置的 ffmpeg 可能因为路径损坏、权限或杀软拦截而无法         正常执行。encoder 探测失败时必须返回 False，, FFmpeg 声明支持某个硬件编码器，不代表当前显卡或驱动一定可用。         首次实际编码失败后，应立即用 libx264 重试，并在本进程禁用该编码 (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (11): RedisTaskManager, {       "video_subject": "",       "video_aspect": "横屏 16:9（西瓜视频）",       "vo, VideoParams, WebUI 新增字幕背景开关和颜色选择器后，所有已有语言都必须包含对应         翻译 key，避免某些语言界面直接显示英文内部 key。, UI 会根据开关向后端传递 False 或颜色字符串。这里验证 schema 仍然         接受这两种值，避免后续依赖或类型调整破坏 WebUI 与合, TextClip 的画布会包含字体行高和 baseline 空白，直接居中画布会让         字幕在背景里看起来偏下。这里用一个假 mask 模拟“可见, 中文长句按字符换行时，句号等闭合标点不能独占一行，否则字幕背景         会被一个单独的小点撑高。这里复现大字号中文长句的边界情况。, TestSubtitleBackgroundSettings (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (18): 兼容 PR #981 曾使用过的 none sentinel，避免少量直接调用 API 的用户         升级后立即失效。新 UI 和新代码仍统一使用, 无配音没有真实 TTS 音频，只能根据脚本文字估算阅读时间。俄语、阿拉伯语、         日文假名、韩文等非 ASCII 文本也必须参与估算，不能都落到最, 即使 FFmpeg 进程返回成功，也要确认输出文件真实存在且非空。这样可以把         异常收敛在 TTS 阶段，而不是拖到后续视频合成阶段才暴露。, 空 voice 通常意味着配置缺失或接口参数错误，不能自动切到无配音模式。         否则用户填错 TTS 配置时也会得到一个“成功”的静音视频，定位成, 验证 Azure TTS V1 在旧版 edge_tts 依赖残留时仍可继续工作。          这个回归场景对应 Windows 便携包更新失败后，现, 验证 Azure TTS V1 在 edge_tts 同步流卡住时能够快速失败。          真实现场里，网络异常、服务端限流、voice 语言与文本, 验证 Gemini TTS 在 edge_tts 7.x 环境下仍会返回项目兼容的字幕结构，         并且可以被 `subtitle_provider, 验证 Xiaomi MiMo TTS 可以消费 OpenAI-compatible 的音频响应结构。          这里用 fake OpenAI cl (+10 more)

### Community 8 - "Community 8"
Cohesion: 0.08
Nodes (17): MaterialInfo, VideoAspect, download_videos(), _download_videos_by_script_order(), get_api_key(), _get_tls_verify(), Coverr (https://coverr.co) - free HD/4K stock videos,     subject to Coverr lic, 按脚本文案顺序下载素材。      默认下载逻辑会把所有关键词的候选素材合并成一个大列表；如果第一个     关键词返回很多结果，最终下载时可能一直消耗这 (+9 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (9): Any, TaskManager, TaskQueueFullError, InMemoryTaskManager, _FakeRequest, endpoint 未显式配置时，任务查询接口不能使用 Host 派生绝对 URL，         也不能把展示 URL 回写到任务状态里，否则不同 Host, 并发数用尽后，等待队列必须有硬上限。这里用 max_concurrent_tasks=0         强制任务进入队列，验证超过 max_queued_t, TestSecurityControls (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (10): ABC, BaseState, MemoryState, Convert values written by this application back to common Python types., Redis-backed task state.      Trust boundary: Redis is expected to be private, RedisState, _FakeRedis, Redis SCAN 分批返回 key 时，分页切片必须按当前批次起始位置计算。          这个用例复现 PR #890 描述的 18 条任务、pa (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.14
Nodes (30): build_script_prompt(), build_social_metadata_prompt(), _clamp_text(), _extract_chat_completion_text(), _extract_qwen_generation_text(), _fallback_social_metadata(), _generate_response(), generate_script() (+22 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (14): download_videos 可能被服务层或测试直接传入字符串模式，而不是         VideoConcatMode 枚举。这里用空搜索词避免真实网络, 开启按文案顺序匹配素材后，不能让第一个关键词的多个候选先把         音频时长填满。这里模拟两个关键词各有多个候选，验证下载顺序是         t, Coverr 视频素材源(spec: 2026-06-09-coverr-video-provider-design.md)。     全部用 unittes, search_videos_coverr 应把每个 hit 转成 MaterialInfo，并把 urls.mp4_download         直接作为, 与 pexels/pixabay 一致:未显式配置时 TLS 校验默认开启。, 企业自签证书代理场景必须能显式关闭 TLS 校验。, Coverr duration 字段在不同响应里可能是 number 或 string,         两种格式都要接受;低于 minimum_durati, 默认路径必须开启 TLS 校验，避免素材 API key 和返回的素材 URL         在公共网络或不可信代理环境中被中间人攻击截获或篡改。 (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.11
Nodes (13): font_dir(), get_ffmpeg_binary(), normalize_script_for_subtitle_matching(), public_dir(), 解析当前进程应该使用的 FFmpeg 可执行文件。      增加原因：     1. 视频编码、静音音频生成、pydub 音频转码都依赖 FFmpeg；, 清理字幕匹配前的脚本文本。      用户可能手动输入 Markdown 分隔符、标题强调或 `_` 这类格式符号。     这些字符通常不会出现在 TT, resource_dir(), root_dir() (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.19
Nodes (9): _get(), _get_all(), _has_key(), _mock_response(), TestUploadPostYouTube, cross_post_video(), Upload-Post API integration for cross-posting videos to TikTok, Instagram and Yo, Check the status of an upload request.          Args:             request_id (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.29
Nodes (11): generate_audio(), generate_final_videos(), generate_script(), generate_subtitle(), generate_terms(), get_video_materials(), Generate audio for the video script.     If a custom audio file is provided, it, Generate subtitle for the video script.     If subtitle generation is disabled (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (8): _can_resolve_hostname(), _decode_linux_route_gateway(), get_container_default_gateway_ip(), get_default_ollama_base_url(), is_running_in_container(), 返回 Ollama 的默认 OpenAI-compatible base_url。      用户显式配置 `ollama_base_url` 时不会走这里, 判断当前进程是否运行在容器内。      这个判断主要用于 Ollama 默认地址选择：     - 普通本机运行时，`localhost` 指向用户机器, 读取 Linux 容器里的默认网关 IP。      Docker Desktop 通常提供 `host.docker.internal`，但原生 Linu

### Community 18 - "Community 18"
Cohesion: 0.31
Nodes (3): _load_translation(), TestWebuiI18n, _TrKeyVisitor

### Community 19 - "Community 19"
Cohesion: 0.25
Nodes (4): Whisper fallback 校正阶段也必须忽略 `---` 这类不可发声脚本行。          如果这里继续保留 Markdown 分隔符，`co, The final subtitle must be parsed even when the SRT file does not end         w, A normal SRT ending in a blank line still parses all blocks., TestSubtitleService

### Community 20 - "Community 20"
Cohesion: 0.53
Nodes (5): Clip, fadein_transition(), fadeout_transition(), slidein_transition(), slideout_transition()

### Community 21 - "Community 21"
Cohesion: 0.53
Nodes (4): correct(), file_to_subtitles(), levenshtein_distance(), similarity()

### Community 32 - "Community 32"
Cohesion: 0.04
Nodes (46): ① إنشاء بيئة Python افتراضية, ① استنساخ المشروع, ① تشغيل حاوية Docker, ② الوصول إلى واجهة الويب, ② تثبيت ImageMagick, ② تعديل ملف الإعدادات, ③ الوصول إلى واجهة الـ API, ③ تشغيل واجهة الويب 🌐 (+38 more)

### Community 33 - "Community 33"
Cohesion: 0.05
Nodes (40): ① Clone the Project, ① Create a Python Virtual Environment, ① Launch the Docker Container, ② Access the Web Interface, ② Launch the Web Interface 🌐, ② Modify the Configuration File, ③ Access the API Interface, ③ Launch the API Service 🚀 (+32 more)

### Community 34 - "Community 34"
Cohesion: 0.05
Nodes (37): ① 克隆代码, ① 创建虚拟环境, ① 启动Docker, ② 修改配置文件（可选，建议启动后也可以在 WebUI 里面配置）, ② 启动Web界面 🌐, ② 访问Web界面, ③ 启动API服务 🚀, ③ 访问API文档 (+29 more)

### Community 35 - "Community 35"
Cohesion: 0.21
Nodes (4): build_video_params(), parse_args(), run_cli(), Namespace

### Community 36 - "Community 36"
Cohesion: 0.17
Nodes (11): 1. React Implementation (`motion/react`), 2. Vanilla JavaScript Implementation (`motion`), Animation Controls, Basic Usage, Basic Usage, Best Practices, Gestures & Hover States, Installation (+3 more)

### Community 37 - "Community 37"
Cohesion: 0.25
Nodes (7): 1. Running Scripts (`uv run`), 2. Managing Environments (`uv venv`), 3. Package Operations (`uv pip`), 4. Tool Execution (`uvx` or `uv tool`), Best Practices, Key Commands, uv (Python Package Manager)

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (6): Firecrawl Skill, Key Capabilities, Single-Page Scraping, Site Crawling, Site Mapping, Usage Reference

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): Configuration (env / config.yaml), Installation & Setup, Key Pipelines, MoneyPrinterTurbo Skill, Option 1: Via Docker (Recommended), Option 2: Local Installation (via uv / pip)

### Community 40 - "Community 40"
Cohesion: 0.33
Nodes (5): Adding New Tests, Directory Structure, MoneyPrinterTurbo Test Directory, Running Tests, Test Resources

### Community 41 - "Community 41"
Cohesion: 0.40
Nodes (4): Key Tools, MCP Tools: code-review-graph, When to use graph tools FIRST, Workflow

### Community 42 - "Community 42"
Cohesion: 0.40
Nodes (4): Debug Issue, Steps, Tips, Token Efficiency Rules

### Community 43 - "Community 43"
Cohesion: 0.40
Nodes (4): Explore Codebase, Steps, Tips, Token Efficiency Rules

### Community 44 - "Community 44"
Cohesion: 0.40
Nodes (4): Key Tools, MCP Tools: code-review-graph, When to use graph tools FIRST, Workflow

### Community 45 - "Community 45"
Cohesion: 0.40
Nodes (4): Disclosure Expectations, Reporting a Vulnerability, Security Policy, Supported Versions

### Community 46 - "Community 46"
Cohesion: 0.40
Nodes (4): Refactor Safely, Safety Checks, Steps, Token Efficiency Rules

### Community 47 - "Community 47"
Cohesion: 0.40
Nodes (4): Output Format, Review Changes, Steps, Token Efficiency Rules

### Community 48 - "Community 48"
Cohesion: 0.40
Nodes (4): Meta Commands, RTK - Rust Token Killer (Google Antigravity), Rule, Why

### Community 49 - "Community 49"
Cohesion: 0.50
Nodes (3): API Key Selection by Shell, General Rules, graphify

## Knowledge Gaps
- **157 isolated node(s):** `crg-session-start.sh script`, `crg-update.sh script`, `_Config`, `moneyprinterturbo`, `webui.sh script` (+152 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `azure_tts_v2()` connect `Community 1` to `Community 11`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `MaterialInfo` connect `Community 8` to `Community 0`, `Community 35`, `Community 3`, `Community 5`, `Community 6`, `Community 9`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `TestVideoService` connect `Community 5` to `Community 8`, `Community 9`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `TestLiteLLMProvider` (e.g. with `VideoScriptRequest` and `VideoSocialMetadataRequest`) actually correct?**
  _`TestLiteLLMProvider` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `TestVideoService` (e.g. with `TaskQueueFullError` and `InMemoryTaskManager`) actually correct?**
  _`TestVideoService` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `VideoParams` (e.g. with `RedisTaskManager` and `.dequeue()`) actually correct?**
  _`VideoParams` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `crg-session-start.sh script`, `crg-update.sh script`, `Application implementation - ASGI.` to the rest of the system?**
  _313 weakly-connected nodes found - possible documentation gaps or missing edges._