/**
 * Nexus Code Playground — React widget embedded in Django templates.
 * Uses React 18 from CDN (no build step).
 */
(function (global) {
  'use strict';

  var React = global.React;
  var ReactDOM = global.ReactDOM;
  var useState = React.useState;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : '';
  }

  function Playground(props) {
    var starter = props.starter || '# Write your code here\nprint("Hello, Nexus AI!")';
    var completeUrl = props.completeUrl || '';
    var _useState = useState(starter);
    var code = _useState[0];
    var setCode = _useState[1];
    var _useState2 = useState('');
    var output = _useState2[0];
    var setOutput = _useState2[1];
    var _useState3 = useState(false);
    var running = _useState3[0];
    var setRunning = _useState3[1];

    function handleRun() {
      setRunning(true);
      setOutput('Running...\n');
      setTimeout(function () {
        setOutput(
          '▶ Output (simulated)\n' +
          '─────────────────────\n' +
          (code.indexOf('print') !== -1 ? 'Hello, Nexus AI!\n' : 'Code executed successfully.\n') +
          '\nTip: Connect a real sandbox API for live execution.'
        );
        setRunning(false);
      }, 600);
    }

    function handleComplete() {
      if (!completeUrl) return;
      var formData = new FormData();
      formData.append('code', code);
      fetch(completeUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData,
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.success) {
            setOutput('✓ Lesson complete! +' + data.xp_reward + ' XP (Level ' + data.level + ')');
            if (typeof gsap !== 'undefined') {
              gsap.from('.playground-output', { scale: 0.98, duration: 0.3 });
            }
          }
        })
        .catch(function () {
          setOutput('Could not mark complete. Try the form submit.');
        });
    }

    return React.createElement(
      'div',
      { className: 'nexus-playground' },
      React.createElement('textarea', {
        className: 'playground-editor',
        value: code,
        onChange: function (e) { setCode(e.target.value); },
        spellCheck: false,
      }),
      React.createElement(
        'div',
        { className: 'playground-toolbar' },
        React.createElement(
          'button',
          { className: 'btn btn-primary btn-sm', onClick: handleRun, disabled: running },
          running ? 'Running...' : '▶ Run code'
        ),
        React.createElement(
          'button',
          { className: 'btn btn-ghost btn-sm', onClick: function () { setCode(starter); } },
          'Reset'
        ),
        React.createElement(
          'button',
          { className: 'btn btn-primary btn-sm', onClick: handleComplete },
          '✓ Complete lesson'
        )
      ),
      React.createElement('pre', { className: 'playground-output' }, output || 'Output will appear here.')
    );
  }

  global.NexusPlayground = {
    mount: function (el) {
      if (!React || !ReactDOM) {
        el.innerHTML = '<p class="text-muted">React failed to load.</p>';
        return;
      }
      var root = ReactDOM.createRoot(el);
      root.render(
        React.createElement(Playground, {
          starter: el.dataset.starter ? el.dataset.starter.replace(/\\n/g, '\n') : '',
          completeUrl: el.dataset.completeUrl || '',
        })
      );
    },
  };
})(window);
