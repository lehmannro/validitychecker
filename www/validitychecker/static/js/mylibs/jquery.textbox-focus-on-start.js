/*
 * textboxFocusOnStart: a jquery-plugin
 * Given a <input type='text'>-Textbox, this plugin make the textbox autofocus on start,
 * along with displaying a certain 'Search me'-text as long as nothing is entered.
 */
(function ($) {
	"use strict";
	/*
	 * Helper-function to position cursor in a textbox.
	 * Works in Chrome and Firefox only.
	 */
	var setCaretPosition = function (ctrl, pos) {
		ctrl.setSelectionRange(pos, pos);
	};

	$.fn.textboxFocusOnStart = function (options) {
		// note: this already refers to jquery-Object, so there is no need for $(this)

		/*
		 * Obviously, only one element can have the focus, so:
		 * Abort, when there is not exactly one.
		 */
		if (this.length !== 1) {
			console.error('The TextboxFocusOnStart-plugin works only with exactly one element given.');
			return;
		}
		// standard settings
		var settings = {
			text: 'Search…',
			cssClassWhenEmpty: 'textbox-empty'
		},
		// get the textbox-dom-element
		    domElement = this.get(0);

		// merge given options into standard-settings
		$.extend(settings, options);

		var displayStandardTextWhenEmpty = function (input) {
			var text  = input.value,
			    $input = $(input);
			/* when textbox is really empty, add css class and set standard text; set cursor */
			if (text === '') {
				$input.addClass(settings.cssClassWhenEmpty).val(settings.text);
				setCaretPosition(input, 0);
			}
		};

		// prepare textbox with given standard text and set focus with cursor at the first position
		this.val(settings.text).addClass(settings.cssClassWhenEmpty);
		domElement.focus();
		setCaretPosition(domElement, 0);

		/* add key-event-handlers for keydown and keyup:
		 * note: in keydown, this.value refers to the value before the keypress,
		 *       while in keyup it refers to the value after the keypress.
		 */
		this.keydown(function (event) {
			var text  = this.value,
			    input = $(this);
			/* When textbox was empty (meaning standard-text) before, and an alphanumerical key was pressed
			 * (0.keyCode = 48 until z.keyCode = 90, see http://www.mediaevent.de/javascript/Extras-Javascript-Keycodes.html
			 * for what key has which keyCode) clear value and apply correct style.
			 */
			if (text === settings.text && event.keyCode >= 48 && event.keyCode <= 90) {
				input.removeClass(settings.cssClassWhenEmpty).val('');
			}
		}).keyup(function () {
			displayStandardTextWhenEmpty(this);
		}).focus(function () {
			var input = $(this);
			input.removeClass(settings.cssClassWhenEmpty);
			// clear input on focus
			if (this.value === settings.text)
				this.value = '';
		}).blur(function () {
			displayStandardTextWhenEmpty(this);
		});
		return this;
	};
}(jQuery));
