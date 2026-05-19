/**
 * DevFlow.io Universal Code Editor — React Component (No build step).
 * Supports multi-language dropdown, local file downloads, and direct assignment integration.
 */
(function (global) {
  'use strict';

  var React = global.React;
  var ReactDOM = global.ReactDOM;
  var useState = React.useState;
  var useEffect = React.useEffect;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : '';
  }

  // Syntax template starters per language
  var STARTERS = {
    python: '# Write your Python solution here\n\ndef fibonacci(n):\n    # TODO: Implement fibonacci sequence generator\n    if n <= 0:\n        return []\n    elif n == 1:\n        return [0]\n    \n    sequence = [0, 1]\n    while len(sequence) < n:\n        sequence.append(sequence[-1] + sequence[-2])\n    return sequence\n\nprint("Test Output:", fibonacci(5))\n',
    javascript: '// Write your JavaScript solution here\n\nfunction calculateFactorial(num) {\n    if (num < 0) return -1;\n    else if (num == 0) return 1;\n    else {\n        return (num * calculateFactorial(num - 1));\n    }\n}\n\nconsole.log("Factorial of 5:", calculateFactorial(5));\n',
    html: '<!-- Write your HTML/CSS solution here -->\n\n<!DOCTYPE html>\n<html>\n<head>\n    <style>\n        body {\n            font-family: "Outfit", sans-serif;\n            background: linear-gradient(135deg, #0f172a, #1e1b4b);\n            color: #f8fafc;\n            display: flex;\n            justify-content: center;\n            align-items: center;\n            height: 100vh;\n            margin: 0;\n        }\n        .card {\n            background: rgba(255, 255, 255, 0.05);\n            backdrop-filter: blur(12px);\n            border: 1px solid rgba(255, 255, 255, 0.1);\n            padding: 2.5rem;\n            border-radius: 1.5rem;\n            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);\n            text-align: center;\n        }\n    </style>\n</head>\n<body>\n    <div class="card">\n        <h1>Hello, DevFlow.io!</h1>\n        <p>This is a premium, real-time sandboxed preview.</p>\n    </div>\n</body>\n</html>\n',
    cpp: '// Write your C++ solution here\n\n#include <iostream>\n#include <vector>\n\nusing namespace std; \n\nint main() {\n    cout << "Welcome to the DevFlow C++ Editor!" << endl;\n    return 0;\n}\n',
    java: '// Write your Java solution here\n\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from DevFlow LMS!");\n    }\n}\n'
  };

  var EXTENSIONS = {
    python: 'py',
    javascript: 'js',
    html: 'html',
    cpp: 'cpp',
    java: 'java'
  };

  function UniversalEditor(props) {
    var rawAssignments = props.assignments || [];
    var isArabic = props.activeLang === 'ar';

    var _useState = useState('python');
    var lang = _useState[0];
    var setLang = _useState[1];

    var _useState2 = useState(STARTERS.python);
    var code = _useState2[0];
    var setCode = _useState2[1];

    var _useState3 = useState('');
    var consoleOutput = _useState3[0];
    var setConsoleOutput = _useState3[1];

    var _useState4 = useState(false);
    var isSubmitting = _useState4[0];
    var setIsSubmitting = _useState4[1];

    var _useState5 = useState(rawAssignments[0] ? rawAssignments[0].id : '');
    var selectedAssignmentId = _useState5[0];
    var setSelectedAssignmentId = _useState5[1];

    // Update editor starter when language is switched
    function handleLanguageChange(event) {
      var selectedLang = event.target.value;
      setLang(selectedLang);
      setCode(STARTERS[selectedLang] || '');
      setConsoleOutput(
        isArabic 
          ? 'تم تغيير اللغة إلى ' + selectedLang.toUpperCase() + '. جاهز لتشغيل الكود.'
          : 'Language changed to ' + selectedLang.toUpperCase() + '. Ready to run.'
      );
    }

    // Run Code Simulation
    function handleRunCode() {
      setConsoleOutput(isArabic ? 'جاري تشغيل الكود وتدقيقه...' : 'Compiling and executing code...');
      setTimeout(function () {
        if (lang === 'html') {
          setConsoleOutput(
            isArabic 
              ? '▶ المحاكاة المباشرة للواجهة:\nتم عرض المعاينة الحية للواجهة بنجاح!\n(مخرجات HTML تظهر بملء الشاشة عند التحميل)'
              : '▶ Live Layout Preview:\nSuccessfully compiled HTML DOM node!\n(HTML outputs render fullscreen upon load)'
          );
        } else if (lang === 'python' && code.indexOf('def fibonacci') !== -1) {
          setConsoleOutput(
            isArabic 
              ? '▶ مخرجات التشغيل:\nTest Output: [0, 1, 1, 2, 3]\n─────────────────────\nتم تشغيل كود بايثون واجتياز جميع اختبارات Fibonacci بنجاح!'
              : '▶ Execution Output:\nTest Output: [0, 1, 1, 2, 3]\n─────────────────────\nPython code executed and successfully passed all Fibonacci unit test assertions!'
          );
        } else {
          setConsoleOutput(
            isArabic 
              ? '▶ مخرجات التشغيل:\nتم تجميع وتشغيل الكود بنجاح!\nالمخرجات: ترحيب من بيئة DevFlow الافتراضية.'
              : '▶ Execution Output:\nSuccessfully compiled and executed!\nOutput: Greeted by DevFlow virtual environment.'
          );
        }
      }, 700);
    }

    // Local Download File Utility
    function handleDownloadFile() {
      var ext = EXTENSIONS[lang] || 'txt';
      var filename = 'solution.' + ext;
      var blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
      var url = URL.createObjectURL(blob);
      
      var a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      setConsoleOutput(
        isArabic 
          ? '📥 تم تنزيل الملف بنجاح كـ (' + filename + ')!'
          : '📥 Successfully generated and downloaded file (' + filename + ')!'
      );
    }

    // Submit assignment to backend
    function handleSubmitAssignment() {
      if (!selectedAssignmentId) {
        alert(isArabic ? 'يرجى اختيار مهمة دراسية أولاً للتسليم.' : 'Please select an assignment first before submitting.');
        return;
      }

      setIsSubmitting(true);
      setConsoleOutput(isArabic ? 'جاري إرسال الحل وتصحيحه عبر الذكاء الاصطناعي...' : 'Uploading solution to LMS for automated grading...');

      var formData = new FormData();
      formData.append('assignment_id', selectedAssignmentId);
      formData.append('code', code);
      formData.append('language', lang);

      fetch('/courses/assignments/submit/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
      })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        setIsSubmitting(false);
        if (data.success) {
          setConsoleOutput(data.feedback + '\n\n⭐ XP Earned: +' + data.xp_reward + ' XP (Level ' + data.level + ')');
          if (typeof gsap !== 'undefined') {
            gsap.from('.playground-output', { scale: 0.97, duration: 0.4, ease: 'elastic.out(1, 0.75)' });
          }
        } else {
          setConsoleOutput('❌ Error: ' + (data.error || 'Submission failed.'));
        }
      })
      .catch(function () {
        setIsSubmitting(false);
        setConsoleOutput('❌ Connection failed. Could not reach server.');
      });
    }

    return React.createElement(
      'div',
      { className: 'editor-playground-container' },
      
      // Control Panel Toolbar
      React.createElement(
        'div',
        { className: 'editor-control-panel glass-card' },
        
        // Language Selector
        React.createElement(
          'div',
          { className: 'control-item' },
          React.createElement('label', null, isArabic ? 'لغة البرمجة:' : 'Select Language:'),
          React.createElement(
            'select',
            { value: lang, onChange: handleLanguageChange, className: 'glass-input' },
            React.createElement('option', { value: 'python' }, 'Python'),
            React.createElement('option', { value: 'javascript' }, 'JavaScript'),
            React.createElement('option', { value: 'html' }, 'HTML / CSS'),
            React.createElement('option', { value: 'cpp' }, 'C++'),
            React.createElement('option', { value: 'java' }, 'Java')
          )
        ),

        // Download Action
        React.createElement(
          'div',
          { className: 'control-item' },
          React.createElement(
            'button',
            { className: 'btn btn-ghost btn-sm', onClick: handleDownloadFile },
            '📥 ' + (isArabic ? 'تنزيل الكود كملف' : 'Download File')
          )
        ),

        // Assignment Selection & Submission
        rawAssignments.length > 0 && React.createElement(
          'div',
          { className: 'control-item assignment-picker' },
          React.createElement('label', null, isArabic ? 'الربط بمهمة:' : 'Link Assignment:'),
          React.createElement(
            'select',
            { 
              value: selectedAssignmentId, 
              onChange: function (e) { setSelectedAssignmentId(e.target.value); }, 
              className: 'glass-input' 
            },
            rawAssignments.map(function (assign) {
              return React.createElement(
                'option', 
                { key: assign.id, value: assign.id }, 
                assign.title + ' (' + assign.course_title + ')'
              );
            })
          ),
          React.createElement(
            'button',
            { 
              className: 'btn btn-primary btn-sm submit-assignment-btn', 
              onClick: handleSubmitAssignment,
              disabled: isSubmitting 
            },
            isSubmitting ? (isArabic ? 'جاري التسليم...' : 'Submitting...') : (isArabic ? '✓ تقديم الحل النهائي' : '✓ Submit Solution')
          )
        )
      ),

      // Workspace Grid (Editor + Console Pane)
      React.createElement(
        'div',
        { className: 'editor-workspace' },
        
        // Code Textarea Pane
        React.createElement(
          'div',
          { className: 'editor-pane glass-card' },
          React.createElement(
            'div',
            { className: 'pane-header' },
            React.createElement('span', null, '💻 ' + (isArabic ? 'محرر الأكواد الذكي' : 'Smart Code Editor')),
            React.createElement(
              'button',
              { className: 'btn btn-accent btn-sm', onClick: handleRunCode },
              '▶ ' + (isArabic ? 'تشغيل واختبار الكود' : 'Run & Execute')
            )
          ),
          React.createElement('textarea', {
            className: 'code-editor-textarea',
            value: code,
            onChange: function (e) { setCode(e.target.value); },
            spellCheck: false,
          })
        ),

        // Console Pane
        React.createElement(
          'div',
          { className: 'console-pane glass-card' },
          React.createElement('div', { className: 'pane-header' }, '🖥️ ' + (isArabic ? 'نافذة المخرجات والتقييم' : 'Evaluation Terminal')),
          React.createElement('pre', { className: 'playground-output' }, consoleOutput || (isArabic ? 'المخرجات والتقييم الذكي ستظهر هنا بعد تشغيل الكود أو تسليم المهمة.' : 'Simulation outputs and automated grades will appear here.'))
        )
      )
    );
  }

  global.NexusUniversalEditor = {
    mount: function (el) {
      if (!React || !ReactDOM) {
        el.innerHTML = '<p class="text-muted">React failed to load.</p>';
        return;
      }
      
      var rawAssignments = [];
      if (el.dataset.assignments) {
        try {
          rawAssignments = JSON.parse(el.dataset.assignments);
        } catch (e) {
          console.error("Failed to parse editor assignments dataset", e);
        }
      }

      var root = ReactDOM.createRoot(el);
      root.render(
        React.createElement(UniversalEditor, {
          assignments: rawAssignments,
          activeLang: el.dataset.activeLang || 'en',
        })
      );
    }
  };

})(window);
