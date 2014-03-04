/* Load this script using conditional IE comments if you need to support IE 7 and IE 6. */

window.onload = function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'icomoon\'">' + entity + '</span>' + html;
	}
	var icons = {
			'icon-location' : '&#xe000;',
			'icon-key' : '&#xe001;',
			'icon-lock' : '&#xe002;',
			'icon-unlocked' : '&#xe003;',
			'icon-notebook' : '&#xe004;',
			'icon-lightbulb' : '&#xe005;',
			'icon-file' : '&#xe006;',
			'icon-facebook' : '&#xe007;',
			'icon-twitter' : '&#xe008;',
			'icon-feed' : '&#xe009;',
			'icon-youtube' : '&#xe00a;',
			'icon-linkedin' : '&#xe00b;',
			'icon-chart' : '&#xe00c;',
			'icon-bookmark' : '&#xe00d;',
			'icon-map-pin-fill' : '&#xe00e;',
			'icon-plus-alt' : '&#xe00f;',
			'icon-address-book' : '&#xe010;',
			'icon-cog' : '&#xe011;',
			'icon-cog-2' : '&#xe012;',
			'icon-user' : '&#xe013;',
			'icon-star' : '&#xe014;',
			'icon-arrow-down' : '&#xe015;',
			'icon-arrow-down-alt1' : '&#xe016;',
			'icon-arrow-right' : '&#xe017;',
			'icon-arrow-left' : '&#xe018;',
			'icon-circle-arrow-left' : '&#xf0a8;',
			'icon-circle-arrow-right' : '&#xf0a9;',
			'icon-circle-arrow-down' : '&#xf0ab;',
			'icon-circle-arrow-up' : '&#xf0aa;',
			'icon-list-ul' : '&#xf0ca;',
			'icon-attachment' : '&#xe019;',
			'icon-attachment-2' : '&#xe01a;',
			'icon-paperclip' : '&#xe01b;',
			'icon-bulb' : '&#xe01c;',
			'icon-profile' : '&#xe01d;',
			'icon-vcard' : '&#xe01e;',
			'icon-users' : '&#xe01f;',
			'icon-users-2' : '&#xe020;',
			'icon-address-book-2' : '&#xe021;',
			'icon-file-alt' : '&#xf0f6;',
			'icon-file-2' : '&#xf016;',
			'icon-podcast' : '&#xe022;',
			'icon-connection' : '&#xe023;',
			'icon-mail' : '&#xe024;',
			'icon-mail-2' : '&#xe025;',
			'icon-help' : '&#xe026;',
			'icon-question' : '&#xe027;',
			'icon-earth' : '&#xe028;',
			'icon-earth-2' : '&#xe029;',
			'icon-note' : '&#xe02a;',
			'icon-user-2' : '&#xe02b;',
			'icon-user-3' : '&#xe02c;',
			'icon-lock2' : '&#xf0eb;',
			'icon-lock-2' : '&#xe02d;'
		},
		els = document.getElementsByTagName('*'),
		i, attr, html, c, el;
	for (i = 0; ; i += 1) {
		el = els[i];
		if(!el) {
			break;
		}
		attr = el.getAttribute('data-icon');
		if (attr) {
			addIcon(el, attr);
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
};