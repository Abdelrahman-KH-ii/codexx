/**
 * Nexus Analytics Chart — React bar chart widget.
 */
(function (global) {
  'use strict';

  var React = global.React;
  var ReactDOM = global.ReactDOM;

  function AnalyticsChart(props) {
    var labels = props.labels || [];
    var minutes = props.minutes || [];
    var maxVal = Math.max.apply(null, minutes.concat([1]));

    return React.createElement(
      'div',
      { className: 'nexus-chart' },
      React.createElement(
        'div',
        { className: 'analytics-bars' },
        labels.map(function (label, i) {
          var h = Math.round((minutes[i] || 0) / maxVal * 140) || 4;
          return React.createElement(
            'div',
            { key: label + i, className: 'analytics-bar-wrap' },
            React.createElement('div', {
              className: 'analytics-bar',
              style: { height: h + 'px' },
              title: (minutes[i] || 0) + ' min',
            }),
            React.createElement('span', { className: 'analytics-bar-label' }, label)
          );
        })
      ),
      React.createElement(
        'p',
        { style: { fontSize: '0.75rem', color: '#64748b', marginTop: '0.5rem' } },
        'Minutes studied per day'
      )
    );
  }

  global.NexusAnalyticsChart = {
    mount: function (el) {
      if (!React || !ReactDOM) return;
      var labels = (el.dataset.labels || '').split(',').filter(Boolean);
      var minutes = (el.dataset.minutes || '').split(',').map(function (v) {
        return parseInt(v, 10) || 0;
      });
      var root = ReactDOM.createRoot(el);
      root.render(React.createElement(AnalyticsChart, { labels: labels, minutes: minutes }));
    },
  };
})(window);
