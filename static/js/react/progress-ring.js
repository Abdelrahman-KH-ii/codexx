/**
 * Nexus Progress Ring — React widget for enrollment progress.
 */
(function (global) {
  'use strict';

  var React = global.React;
  var ReactDOM = global.ReactDOM;

  function ProgressRing(props) {
    var percent = Math.min(100, Math.max(0, props.percent || 0));
    var size = props.size || 56;
    var stroke = 4;
    var radius = (size - stroke) / 2;
    var circumference = 2 * Math.PI * radius;
    var offset = circumference - (percent / 100) * circumference;

    return React.createElement(
      'svg',
      {
        className: 'progress-ring',
        width: size,
        height: size,
        viewBox: '0 0 ' + size + ' ' + size,
      },
      React.createElement('circle', {
        cx: size / 2,
        cy: size / 2,
        r: radius,
        fill: 'none',
        stroke: '#e2e8f0',
        strokeWidth: stroke,
      }),
      React.createElement('circle', {
        cx: size / 2,
        cy: size / 2,
        r: radius,
        fill: 'none',
        stroke: 'url(#ring-gradient)',
        strokeWidth: stroke,
        strokeDasharray: circumference,
        strokeDashoffset: offset,
        strokeLinecap: 'round',
        transform: 'rotate(-90 ' + size / 2 + ' ' + size / 2 + ')',
        style: { transition: 'stroke-dashoffset 0.8s ease' },
      }),
      React.createElement(
        'defs',
        null,
        React.createElement(
          'linearGradient',
          { id: 'ring-gradient', x1: '0%', y1: '0%', x2: '100%', y2: '0%' },
          React.createElement('stop', { offset: '0%', stopColor: '#22d3ee' }),
          React.createElement('stop', { offset: '100%', stopColor: '#8b5cf6' })
        )
      ),
      React.createElement(
        'text',
        {
          x: '50%',
          y: '50%',
          textAnchor: 'middle',
          dy: '0.35em',
          className: 'progress-ring-label',
          fontSize: '12',
          fontWeight: '600',
          fill: '#0f172a',
        },
        percent + '%'
      )
    );
  }

  global.NexusProgressRing = {
    mount: function (el, percent) {
      if (!React || !ReactDOM) return;
      var root = ReactDOM.createRoot(el);
      root.render(React.createElement(ProgressRing, { percent: percent }));
    },
  };
})(window);
