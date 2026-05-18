/**
 * Nexus AI Chat — React widget embedded in Django templates.
 * Upgraded with full bilingual support (Arabic & English) for all UI strings and 20 Q&A presets.
 */
(function (global) {
  'use strict';

  var React = global.React;
  var ReactDOM = global.ReactDOM;
  var useState = React.useState;
  var useEffect = React.useEffect;
  var useRef = React.useRef;

  var STRINGS = {
    ar: {
      title: "DevFlow AI Assistant",
      emptyDesc: "مرحباً بك! اختر أحد الأسئلة الجاهزة والمصنفة من لوحة المكتبة البرمجية على اليمين للإجابة الفورية، أو اكتب سؤالك البرمجي المخصص بالأسفل لتشغيل محرك الذكاء الاصطناعي المباشر!",
      libraryTitle: "مكتبة الأسئلة المبرمجة",
      thinking: "Nexus AI يكتب الآن...",
      placeholder: "اكتب سؤالك البرمجي هنا أو تصفح مكتبة الأسئلة المسبقة...",
      speakBtn: "انطق",
      copyBtn: "نسخ",
      copied: "تم النسخ!",
      filterAll: "الكل",
      filterAi: "AI",
      filterWeb: "ويب",
      filterEng: "هندسة",
      filterCareer: "مهنة",
      wrong: "حدث خطأ ما أثناء الاتصال بالسيرفر. يرجى المحاولة مرة أخرى."
    },
    en: {
      title: "DevFlow AI Assistant",
      emptyDesc: "Welcome! Select a preset question from the Library panel on the right for instant replies, or type a custom programming query below to consult the live generative AI assistant!",
      libraryTitle: "Preset Q&A Library",
      thinking: "Nexus AI is typing...",
      placeholder: "Type your programming query here or browse preset questions...",
      speakBtn: "Speak",
      copyBtn: "Copy",
      copied: "Copied!",
      filterAll: "All",
      filterAi: "AI",
      filterWeb: "Web",
      filterEng: "Engineering",
      filterCareer: "Career",
      wrong: "Something went wrong. Please try again."
    }
  };

  var PRESETS = {
    ar: [
      { q: "ما هي أفضل لغات البرمجة للمبتدئين للبدء في 2026؟", a: "تعتبر Python وJavaScript أفضل الخيارات للمبتدئين نظراً لسهولتها وتنوع استخداماتها الشديد في مجالات الذكاء الاصطناعي، وتحليل البيانات، وتطوير واجهات وتطبيقات الويب الكاملة.", c: "career" },
      { q: "كيف أبدأ في مجال الذكاء الاصطناعي وتطوير النماذج؟", a: "ابدأ بتعلم لغة Python بشكل متقن، ثم أساسيات الرياضيات الجبرية والإحصاء، تليها مكتبات تعلم الآلة مثل Scikit-Learn، ثم انتقل للشبكات العصبية العميقة باستخدام PyTorch أو TensorFlow، وتابع بناء المشاريع العملية.", c: "ai" },
      { q: "ما هو مفهوم الـ RAG (Retrieval-Augmented Generation)؟", a: "هي تقنية متطورة لربط النماذج اللغوية الكبيرة (LLMs) بقواعد بيانات خارجية مخصصة (مثل مستندات الشركة) لاستخراج معلومات دقيقة ومحدثة سياقياً، مما يمنع الهلوسة البرمجية دون الحاجة لإعادة تدريب النموذج بالكامل.", c: "ai" },
      { q: "ما هو الـ Prompt Engineering وكيف أستفيد منه؟", a: "هو علم صياغة وتصميم المدخلات والتعليمات الموجهة للنماذج اللغوية (مثل GPT) للحصول على إجابات دقيقة ومتوقعة ومثالية. يفيدك في أتمتة الأعمال وبناء تطبيقات برمجية ذكية تتفاعل بكفاءة مع المستخدمين.", c: "ai" },
      { q: "ما الفرق بين التعلم العميق والتعلم التقليدي؟", a: "التعلم التقليدي يعتمد على خوارزميات إحصائية وميزات يتم استخراجها يدوياً من البيانات بواسطة المهندسين، بينما التعلم العميق (Deep Learning) يستخدم شبكات عصبونية اصطناعية عميقة تستخرج الميزات وتتعلم ذاتياً من البيانات الضخمة.", c: "ai" },
      { q: "كيف تؤثر أدوات الذكاء الاصطناعي على عمل المبرمجين؟", a: "الذكاء الاصطناعي هو مساعد خارق يزيد من سرعة كتابة الكود وحل الأخطاء (Debugging) بنسبة 40%، لكنه لا يلغي دور المبرمجين مطلقاً؛ فالقيمة الحقيقية تكمن في التفكير المنطقي، وهندسة المعمارية، وحل المشكلات المعقدة.", c: "ai" },
      { q: "ما هو الفرق الرئيسي بين الـ Frontend والـ Backend؟", a: "الـ Frontend هو كل ما يراه المستخدم ويتفاعل معه بصرياً في المتصفح (مبني بـ HTML/CSS/React)، بينما الـ Backend هو المحرك الخلفي للموقع الذي يدير قواعد البيانات، والتحقق من الصلاحيات، والمنطق البرمجي (مبني بـ Django/Node.js).", c: "web" },
      { q: "كيف يمكنني تسريع أداء قاعدة بيانات SQLite محلياً؟", a: "1. قم بإنشاء فهارس (Indexes) على الأعمدة المستعمل عنها بكثرة.\n2. فعل وضع WAL (Write-Ahead Logging).\n3. استخدم المعاملات الجماعية (Bulk/Batch operations).\n4. تجنب استعلامات N+1 عبر استخدام select_related و prefetch_related في Django.", c: "web" },
      { q: "ما هي أهم مميزات إطار عمل Django في تطوير الخلفية؟", a: "Django هو إطار عمل متكامل (Batteries-Included) يوفر نظام أمان متطوراً تلقائياً ضد الاختراقات، ونظام مصادقة مستخدمين جاهز، وقاعدة بيانات ORM قوية جداً، بالإضافة للوحة تحكم آدمن مدمجة واحترافية بدون كتابة كود إضافي.", c: "web" },
      { q: "كيف يعمل الـ Event Loop في بيئة Node.js؟", a: "هو آلية تسمح لـ Node.js بتنفيذ عمليات إدخال وإخراج غير حاصرة (Non-blocking I/O) على الرغم من كونها خيطاً وحداً (Single-threaded)، وذلك عبر نقل المهام الثقيلة لنظام التشغيل واستقبالها عبر طابور الكولباك (Callback Queue).", c: "web" },
      { q: "كيف أختار المناسب بين قواعد البيانات SQL و NoSQL؟", a: "اختر SQL (مثل PostgreSQL/SQLite) إذا كانت البيانات ذات هيكل واضح وعلاقات مترابطة وتتطلب ضمان سلامة المعاملات (ACID). اختر NoSQL (مثل MongoDB) للبيانات غير المنظمة، والمشاريع سريعة التطور التي تتطلب توسعاً أفقياً ضخماً.", c: "web" },
      { q: "ما هي النصيحة الذهبية لتجنب كتابة كود معقد (Spaghetti Code)؟", a: "طبق مبدأ المسؤولية الواحدة (Single Responsibility) بحيث تقوم كل دالة أو كلاس بمهمة واحدة فقط، استخدم أسماء متغيرات واضحة ومعبرة، اكتب اختبارات تلقائية (Unit Tests)، وقم إعادة صياغة الكود (Refactoring) دورياً.", c: "eng" },
      { q: "ما فائدة استخدام معمارية الـ Islands Architecture في الويب؟", a: "تسمح ببناء صفحات ويب فائق السرعة وخفيفة الحجم عن طريق تقديم كود HTML ساكن ومبني بالكامل من الخادم، مع زرع أجزاء تفاعلية ديناميكية صغيرة ونشطة (React Islands) فقط في الأماكن التي تتطلب تفاعلاً حياً.", c: "eng" },
      { q: "ما هو مفهوم الـ CI/CD في هندسة البرمجيات؟", a: "هو التكامل المستمر والنشر المستمر (Continuous Integration & Continuous Deployment)؛ ويعني أتمتة عمليات فحص جودة الكود، وتشغيل الاختبارات التلقائية، وبناء المشروع، ونشره في سيرفر الإنتاج فور رفع التحديثات.", c: "eng" },
      { q: "كيف أتعامل مع الأخطاء ومشاكل الكود بذكاء (Debugging)؟", a: "1. اقرأ رسالة الخطأ وتتبع سطر حدوثها بعناية.\n2. قم بعزل المشكلة وتجربة الكود في بيئة معزولة (Scratch script).\n3. استخدم أدوات تتبع الكود (Breakpoints).\n4. أضف سجلات تتبع ذكية (Logging) لمعاينة قيم المتغيرات حياً.", c: "eng" },
      { q: "ما هو الـ API وما هي أنواعه الأكثر استخداماً؟", a: "هو واجهة برمجية (Application Programming Interface) تسمح لتطبيقين بالتواصل وتبادل البيانات. أشهر أنواعه: REST APIs المستندة لبروتوكول HTTP وتنسيق JSON، و GraphQL التي تتيح جلب بيانات محددة بدقة طلب واحد.", c: "eng" },
      { q: "كيف أستعد بشكل احترافي لمقابلات العمل التقنية؟", a: "تمرن على حل الخوارزميات وهياكل البيانات (Data Structures)، وافهم أساسيات هندسة الأنظمة (System Design)، واحرص على فهم الكود الذي كتبته في مشاريعك السابقة لتشرح قراراتك الهندسية بوضوح وثقة.", c: "career" },
      { q: "ما هو الفرق الأساسي بين نظامي Git و GitHub؟", a: "الـ Git هو أداة برمجية محلية تُنصّب على جهازك لتتبع التغييرات في ملفات مشروعك (Version Control System)، بينما الـ GitHub هو منصة سحابية لاستضافة مستودعات Git ومشاركة الكود والتعاون البرمجي مع الآخرين.", c: "career" },
      { q: "كيف أحمي تطبيقات الويب الخاصة بي من هجمات الاختراق؟", a: "استخدم بروتوكول الاتصال الآمن HTTPS، فعل حماية الـ CSRF في النماذج، قم بتصفية والتحقق من مدخلات المستخدمين لمنع هجمات الـ XSS وحقن الـ SQL، وقم بتشير كلمات المرور باستخدام خوارزميات هاش قوية مثل Bcrypt.", c: "career" },
      { q: "كيف أتغلب على متلازمة المحتال (Imposter Syndrome)؟", a: "تذكر دائماً أن البرمجة هي مجال واسع للغاية ومتغير يومياً، ولا أحد يعرف كل شيء. ركز على تقدمك الشخصي اليومي مقارنة بالأمس، وابدأ ببناء مشاريع صغيرة متكاملة وشاركها مع زملائك ومجتمعات المطورين.", c: "career" }
    ],
    en: [
      { q: "What are the best programming languages for beginners to start in 2026?", a: "Python and JavaScript are widely considered the best languages for beginners due to their high readability, gentle learning curves, and absolute versatility in Artificial Intelligence, data analysis, and full-stack web development.", c: "career" },
      { q: "How do I start in Artificial Intelligence and model development?", a: "Begin by mastering Python, followed by essential linear algebra, calculus, and statistics. Then learn ML libraries like Scikit-Learn before diving into Deep Neural Networks using PyTorch or TensorFlow, and focus heavily on practical projects.", c: "ai" },
      { q: "What is the concept of RAG (Retrieval-Augmented Generation)?", a: "RAG is an advanced architecture that connects Large Language Models (LLMs) to custom, external data sources (like private company documents) to retrieve contextually accurate and highly precise information, effectively preventing AI hallucinations without needing full retraining.", c: "ai" },
      { q: "What is Prompt Engineering and how do I benefit from it?", a: "Prompt Engineering is the science of designing inputs and instructions for LLMs to generate highly predictable, optimal, and precise outputs. It is essential for automating tasks and building intelligent products that communicate seamlessly.", c: "ai" },
      { q: "What is the difference between Deep Learning and traditional ML?", a: "Traditional Machine Learning relies on statistical algorithms and features manually extracted from data by engineers. Deep Learning uses deep artificial neural networks (layers of neurons) to automatically extract features and learn patterns from massive, complex datasets.", c: "ai" },
      { q: "How do AI tools affect software developers' careers?", a: "AI is a superpower assistant that boosts coding speed and debugging efficiency by up to 40%. It will never replace developers; instead, it raises the bar, prioritizing logical thinking, system architecture design, and complex problem-solving.", c: "ai" },
      { q: "What is the main difference between Frontend and Backend?", a: "Frontend refers to everything a user visually interacts with inside the browser (built with HTML, CSS, React). Backend is the behind-the-scenes engine that manages databases, handles authentication, and performs the server-side business logic (built with Django, Node.js).", c: "web" },
      { q: "How can I speed up SQLite database performance locally?", a: "1. Create Indexes on columns frequently used in queries.\n2. Enable WAL (Write-Ahead Logging) mode.\n3. Wrap bulk operations inside single, explicit database Transactions.\n4. Avoid N+1 query problems in Django using select_related and prefetch_related.", c: "web" },
      { q: "What are the main advantages of using Django for backend development?", a: "Django is a mature, 'batteries-included' framework. It automatically enforces advanced security protocols (protecting against CSRF, SQL injections), provides robust user authentication out of the box, offers a rich database ORM, and renders a complete Admin Dashboard automatically.", c: "web" },
      { q: "How does the Event Loop work in Node.js?", a: "The Event Loop allows Node.js to execute non-blocking, asynchronous I/O operations despite being single-threaded. It offloads heavy tasks to the OS kernel and processes their associated callbacks sequentially using the Callback Queue.", c: "web" },
      { q: "How do I choose between SQL and NoSQL databases?", a: "Choose SQL (e.g., PostgreSQL/SQLite) if your data structure is relational, strict, and requires full ACID transaction guarantees. Choose NoSQL (e.g., MongoDB) for unstructured or semi-structured data, rapid prototyping, and extreme horizontal scaling requirements.", c: "web" },
      { q: "What is the golden advice to avoid Spaghetti Code?", a: "Adhere closely to the Single Responsibility Principle (functions/classes should do only one thing), use descriptive and semantic names, write comprehensive automated unit tests, and perform regular, iterative code refactoring.", c: "eng" },
      { q: "What is the benefit of using Islands Architecture in web development?", a: "It enables building blazing-fast, lightweight web pages by rendering completely static HTML on the server and hydrating small, dynamic interactive components ('React Islands') only where and when client-side interactivity is actually needed.", c: "eng" },
      { q: "What is the concept of CI/CD in software engineering?", a: "CI/CD stands for Continuous Integration and Continuous Deployment. It is the automated pipeline that runs code quality checks, executes test suites, compiles the build, and deploys updates to production servers immediately upon new code commits.", c: "eng" },
      { q: "How do I handle errors and debug my code smartly?", a: "1. Read the error trace stack and trace the exact line number.\n2. Isolate the issue inside a scratch file.\n3. Utilize debugging breakpoints to inspect runtime states.\n4. Write clear logging markers to verify variable values dynamically.", c: "eng" },
      { q: "What is an API and what are its most common types?", a: "An API (Application Programming Interface) allows two distinct applications to communicate and exchange data. The most common types are REST APIs (HTTP methods returning JSON) and GraphQL APIs (allowing clients to request exact fields in a single call).", c: "eng" },
      { q: "How do I prepare professionally for technical coding interviews?", a: "Master core algorithms and data structures, study system design paradigms, and ensure you can thoroughly explain the technical decisions, trade-offs, and architectures of your previous projects with absolute clarity.", c: "career" },
      { q: "What is the essential difference between Git and GitHub?", a: "Git is a local, offline version control command-line utility used to track history and changes in your project. GitHub is a cloud-based hosting provider for Git repositories that enables sharing, team collaboration, and automated pipelines.", c: "career" },
      { q: "How do I protect my web applications from common cyber hacks?", a: "Always enforce HTTPS, enable CSRF protection on forms, validate and sanitize user inputs to prevent XSS and SQL injections, and securely hash user passwords using strong algorithms like Bcrypt.", c: "career" },
      { q: "How do I overcome Imposter Syndrome as a developer?", a: "Remind yourself that software engineering is a vast and rapidly evolving field; no one knows everything. Focus on your daily incremental growth, build end-to-end projects, and share your learning milestones with developer communities.", c: "career" }
    ]
  };

  function playBeep(type) {
    try {
      var ctx = new (window.AudioContext || window.webkitAudioContext)();
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      
      if (type === 'send') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(580, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1160, ctx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.04, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
        osc.start();
        osc.stop(ctx.currentTime + 0.12);
      } else if (type === 'recv') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(780, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(980, ctx.currentTime + 0.08);
        osc.frequency.exponentialRampToValueAtTime(1380, ctx.currentTime + 0.22);
        gain.gain.setValueAtTime(0.05, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.22);
        osc.start();
        osc.stop(ctx.currentTime + 0.22);
      }
    } catch (e) { /* ignore */ }
  }

  function speakText(text, lang) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      var utterance = new SpeechSynthesisUtterance(text);
      if (lang === 'ar' || /[\u0600-\u06FF]/.test(text)) {
        utterance.lang = 'ar-SA';
      } else {
        utterance.lang = 'en-US';
      }
      utterance.rate = 1.05;
      utterance.volume = 0.85;
      window.speechSynthesis.speak(utterance);
    }
  }

  function copyToClipboard(text, btn, copiedStr) {
    navigator.clipboard.writeText(text).then(function() {
      var original = btn.innerHTML;
      btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:14px; vertical-align:middle;">done</span> ' + copiedStr;
      setTimeout(function() {
        btn.innerHTML = original;
      }, 1500);
    });
  }

  function ChatWidget(props) {
    var sendUrl = props.sendUrl;
    var conversationId = props.conversationId;
    var csrfToken = props.csrfToken;
    var initialMessages = props.initialMessages || [];

    var _useState = useState(initialMessages);
    var messages = _useState[0];
    var setMessages = _useState[1];
    
    var _useState2 = useState('');
    var input = _useState2[0];
    var setInput = _useState2[1];
    
    var _useState3 = useState(false);
    var loading = _useState3[0];
    var setLoading = _useState3[1];
    
    var _useState4 = useState(conversationId || null);
    var convId = _useState4[0];
    var setConvId = _useState4[1];
    
    var _useState5 = useState('all');
    var activeFilter = _useState5[0];
    var setActiveFilter = _useState5[1];

    var _useState6 = useState(localStorage.getItem('nexus_lang') || 'ar');
    var lang = _useState6[0];
    var setLang = _useState6[1];
    
    var bottomRef = useRef(null);

    // Watch for dynamic language switching event
    useEffect(function () {
      function handleLangChange(e) {
        setLang(e.detail);
      }
      window.addEventListener('nexusLanguageChanged', handleLangChange);
      return function () {
        window.removeEventListener('nexusLanguageChanged', handleLangChange);
      };
    }, []);

    useEffect(function () {
      if (bottomRef.current) {
        bottomRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    }, [messages]);

    function handlePresetClick(preset) {
      if (loading) return;
      
      playBeep('send');
      setMessages(function (prev) {
        return prev.concat([{ role: 'user', content: preset.q }]);
      });
      setLoading(true);

      setTimeout(function () {
        playBeep('recv');
        setMessages(function (prev) {
          return prev.concat([
            { role: 'assistant', content: preset.a }
          ]);
        });
        setLoading(false);
      }, 700);
    }

    function sendMessage() {
      var text = input.trim();
      if (!text || loading) return;

      setInput('');
      setLoading(true);
      playBeep('send');
      
      setMessages(function (prev) {
        return prev.concat([{ role: 'user', content: text }]);
      });

      fetch(sendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          message: text,
          conversation_id: convId,
        }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          playBeep('recv');
          if (data.conversation_id) setConvId(data.conversation_id);
          setMessages(function (prev) {
            return prev.concat([
              { role: 'assistant', content: data.assistant_message.content },
            ]);
          });
        })
        .catch(function () {
          var str = STRINGS[lang] || STRINGS.ar;
          setMessages(function (prev) {
            return prev.concat([
              { role: 'assistant', content: str.wrong },
            ]);
          });
        })
        .finally(function () {
          setLoading(false);
        });
    }

    function handleKey(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    }

    var strings = STRINGS[lang] || STRINGS.ar;
    var presetsList = PRESETS[lang] || PRESETS.ar;

    var filteredPresets = presetsList.filter(function (p) {
      if (activeFilter === 'all') return true;
      return p.c === activeFilter;
    });

    var isAr = (lang === 'ar');

    return React.createElement(
      'div',
      { className: 'nexus-chat-container', style: { direction: isAr ? 'rtl' : 'ltr' } },
      
      // Main Chat section
      React.createElement(
        'div',
        { className: 'chat-main-widget' },
        React.createElement(
          'div',
          { className: 'chat-messages-container' },
          messages.length === 0 &&
            React.createElement(
              'div',
              { className: 'chat-empty-slate' },
              React.createElement('span', { className: 'material-symbols-outlined empty-icon' }, 'smart_toy'),
              React.createElement('h3', null, strings.title),
              React.createElement('p', null, strings.emptyDesc)
            ),
          messages.map(function (msg, i) {
            var bubbleIsAr = isAr;
            if (msg.role === 'user') {
              bubbleIsAr = /[\u0600-\u06FF]/.test(msg.content);
            }
            return React.createElement(
              'div',
              { key: i, className: 'chat-msg-wrapper ' + msg.role, style: { alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' } },
              React.createElement(
                'div',
                {
                  className: 'chat-bubble',
                  style: {
                    direction: bubbleIsAr ? 'rtl' : 'ltr',
                    textAlign: bubbleIsAr ? 'right' : 'left'
                  }
                },
                msg.content
              ),
              msg.role === 'assistant' &&
                React.createElement(
                  'div',
                  { className: 'msg-actions-row', style: { justifyContent: isAr ? 'flex-start' : 'flex-start' } },
                  React.createElement(
                    'button',
                    {
                      className: 'msg-act-btn',
                      onClick: function () { speakText(msg.content, lang); }
                    },
                    React.createElement('span', { className: 'material-symbols-outlined' }, 'volume_up'),
                    strings.speakBtn
                  ),
                  React.createElement(
                    'button',
                    {
                      className: 'msg-act-btn',
                      onClick: function (e) { copyToClipboard(msg.content, e.currentTarget, strings.copied); }
                    },
                    React.createElement('span', { className: 'material-symbols-outlined' }, 'content_copy'),
                    strings.copyBtn
                  )
                )
            );
          }),
          loading &&
            React.createElement(
              'div',
              { className: 'chat-msg-wrapper assistant', style: { alignItems: 'flex-start' } },
              React.createElement(
                'div',
                { className: 'chat-bubble thinking-bubble' },
                React.createElement('span', { className: 'thinking-dot' }),
                React.createElement('span', null, strings.thinking)
              )
            ),
          React.createElement('div', { ref: bottomRef })
        ),
        
        React.createElement(
          'div',
          { className: 'chat-input-wrapper' },
          React.createElement('textarea', {
            className: 'chat-input-textarea glass-input',
            rows: 2,
            placeholder: strings.placeholder,
            value: input,
            onChange: function (e) { setInput(e.target.value); },
            onKeyDown: handleKey,
            disabled: loading,
            style: { direction: isAr ? 'rtl' : 'ltr', textAlign: isAr ? 'right' : 'left' }
          }),
          React.createElement(
            'button',
            {
              className: 'btn btn-primary chat-send-btn',
              onClick: sendMessage,
              disabled: loading || !input.trim()
            },
            React.createElement('span', { className: 'material-symbols-outlined' }, isAr ? 'arrow_back' : 'arrow_forward')
          )
        )
      ),

      // Library Presets Sidebar
      React.createElement(
        'div',
        { className: 'chat-presets-sidebar' },
        React.createElement(
          'div',
          { className: 'sidebar-header-preset' },
          React.createElement('span', { className: 'material-symbols-outlined side-icon' }, 'library_books'),
          React.createElement('h4', null, strings.libraryTitle)
        ),
        
        // Category Filters Row
        React.createElement(
          'div',
          { className: 'filter-chips-row' },
          [
            { id: 'all', label: strings.filterAll },
            { id: 'ai', label: strings.filterAi },
            { id: 'web', label: strings.filterWeb },
            { id: 'eng', label: strings.filterEng },
            { id: 'career', label: strings.filterCareer }
          ].map(function (chip) {
            return React.createElement(
              'button',
              {
                key: chip.id,
                className: 'filter-chip ' + (activeFilter === chip.id ? 'active' : ''),
                onClick: function () { setActiveFilter(chip.id); }
              },
              chip.label
            );
          })
        ),

        // Scrollable presets cards list
        React.createElement(
          'div',
          { className: 'presets-list-scrollable' },
          filteredPresets.map(function (preset, idx) {
            return React.createElement(
              'div',
              {
                key: idx,
                className: 'preset-item-card glass-card',
                onClick: function () { handlePresetClick(preset); }
              },
              React.createElement(
                'div',
                { className: 'preset-q-header', style: { flexDirection: isAr ? 'row' : 'row-reverse' } },
                React.createElement('span', { className: 'preset-category-tag tag-' + preset.c }, preset.c.toUpperCase()),
                React.createElement('span', { className: 'material-symbols-outlined preset-arrow' }, isAr ? 'chevron_left' : 'chevron_right')
              ),
              React.createElement('p', { className: 'preset-question-txt', style: { textAlign: isAr ? 'right' : 'left' } }, preset.q)
            );
          })
        )
      )
    );
  }

  global.NexusAIChat = {
    mount: function (el) {
      if (!React || !ReactDOM) {
        el.innerHTML = '<p>React failed to load.</p>';
        return;
      }

      var initial = [];
      try {
        var scriptEl = document.getElementById('chat-initial-messages');
        if (scriptEl) {
          initial = JSON.parse(scriptEl.textContent);
        }
      } catch (e) { /* ignore */ }

      var root = ReactDOM.createRoot(el);
      root.render(
        React.createElement(ChatWidget, {
          sendUrl: el.dataset.sendUrl,
          conversationId: el.dataset.conversationId || null,
          csrfToken: el.dataset.csrf,
          initialMessages: initial.map(function (m) {
            return { role: m.role, content: m.content };
          }),
        })
      );
    },
  };
})(window);
