function setBGColour (bgColour) {
	$('body').css('background', bgColour);
}

// Dynamically add stylesheet rules -- https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleSheet.insertRule
function addStylesheetRules (rules) {
  var styleEl = document.createElement('style'),
      styleSheet;

  // Apparently some version of Safari needs the following line
  styleEl.appendChild(document.createTextNode(''));

  // Append style element to head
  document.head.appendChild(styleEl);

  // console.log(styleEl.sheet);
  // Grab style sheet
  styleSheet = styleEl.sheet

  for (var i = 0, rl = rules.length; i < rl; i++) {
    var j = 1, rule = rules[i], selector = rules[i][0], propStr = '';
    // If the second argument of a rule is an array of arrays, correct our variables.
    if (Object.prototype.toString.call(rule[1][0]) === '[object Array]') {
      rule = rule[1];
      j = 0;
    }

    for (var pl = rule.length; j < pl; j++) {
      var prop = rule[j];
      propStr += prop[0] + ':' + prop[1] + (prop[2] ? ' !important' : '') + ';\n';
    }

    // Insert CSS Rule
    addCSSRule(styleSheet, selector, propStr, styleSheet.cssRules.length);
  }
}


function addCSSRule(sheet, selector, rules, index) {
	if("insertRule" in sheet) {
		sheet.insertRule(selector + "{" + rules + "}", index);
	}
	else if("addRule" in sheet) {
		sheet.addRule(selector, rules, index);
	}
}

