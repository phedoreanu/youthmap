;
(function ($, window, document) {
    $.fn.zLightAccordion = function (options) {
        var setting = $.extend({
            accordionWidth: '50%',
            accordionMinWidth: '0',
            handler: 'click',
            activeSwitch: 'off',
            activeNumber: 'first',
            deploymentSpeed: 1000,
            foldingSpeed: 500,
            headerHeight: 'auto',
            headerBcolor: '#474747',
            headerColor: '#fff',
            headerFontSize: '18px',
            headerPadding: '0',
            iconHeaderUrl: false,
            activeSectionBcolor: '#fff',
            sectionBcolor: '#fff',
            sectionActiveTextColor: '#474747',
            sectionTextColor: '#474747',

            contentColor: '#474747',
            borderWidth: '1px',
            borderStyle: 'solid',
            borderColor: '#dcdcdc',
            iconSwitchUrl: 'ch_right.png',
            iconSwitchUrl2: 'ch_down.png',
            easingEffect: 'easeOutExpo'
        }, options);
        var getAttrVal = this.attr('id'),
            $body = $('body'),
            $html = $('html');
        return this.each(function () {
            var $this = $(this),
                zl_li = $this.find('li'),
                active_number, d_switch = 'switch',
                d_off = 'off',
                d_on = 'on',
                d_header = ':header',
                style_border_li = ' ' + setting.borderWidth + ' ' + setting.borderStyle + ' ' + setting.borderColor + '  ',
                ifImg;
            (!setting.iconHeaderUrl === false) ? ifImg = 'background-image: url(css/img/' + setting.iconHeaderUrl + ');' : ifImg = '';
            var styleAccordion = $('<style type="text/css">	#' + getAttrVal + '{width: ' + setting.accordionWidth + ';min-width:' + setting.accordionMinWidth + ';} #' + getAttrVal + ' > .zl_header{padding:' + setting.headerPadding + ';font-size:' + setting.headerFontSize + ';height:' + setting.headerHeight + '; ' + ifImg + ' background-color: ' + setting.headerBcolor + ';color: ' + setting.headerColor + '; } #' + getAttrVal + ' > .zl_acc{border-left:' + style_border_li + ';border-right:' + style_border_li + ';border-bottom:' + style_border_li + ';} #' + getAttrVal + ' > .zl_acc > li{background-color: ' + setting.sectionBcolor + ' ;border-top:' + style_border_li + ';} #' + getAttrVal + ' > .zl_acc > li > div{background-color: ' + setting.contentBcolor + '; color: ' + setting.contentColor + ' ;} #' + getAttrVal + ' > .zl_acc > li > h1, #' + getAttrVal + ' > .zl_acc > li > h2, #' + getAttrVal + ' > .zl_acc > li > h3, #' + getAttrVal + ' > .zl_acc > li > h4, #' + getAttrVal + ' > .zl_acc > li > h5, #' + getAttrVal + ' > .zl_acc > li > h6{color: ' + setting.sectionTextColor + ' ;} #' + getAttrVal + ' </style>');
            $('html > head').append(styleAccordion);
            if (setting.activeSwitch === 'on') {
                switch (setting.activeNumber) {
                    case 'first':
                        active_number = '0';
                        break;
                    case 'last':
                        active_number = '-1';
                        break;
                    case setting.activeNumber:
                        active_number = setting.activeNumber - 1;
                        break
                };
                zl_li.eq(active_number).css('background-color', setting.activeSectionBcolor).find('div').data(d_switch, d_on).stop(true, true).slideDown().end().children(d_header).css('color', setting.sectionActiveTextColor).addClass('zl_img_switch')
            };
            zl_li.children(d_header).on(setting.handler + '.zl_handler', function () {
                var $self = $(this),
                    zl_div = $self.siblings('div');

                function fufEvents($self, zl_div) {
                    $self.addClass('zl_img_switch').css('color', setting.sectionActiveTextColor).siblings('div').stop(true, true).slideDown(setting.deploymentSpeed, setting.easingEffect).data(d_switch, d_on).end().parent('li').css('background-color', setting.activeSectionBcolor).siblings('li').css('background-color', '').children(d_header).removeClass('zl_img_switch').css('color', '').siblings('div').stop(true, true).slideUp(setting.foldingSpeed, setting.easingEffect).data(d_switch, d_off)
                };
                if (setting.handler === 'click') {
                    (zl_div.data(d_switch) === d_off || !zl_div.data(d_switch)) ? fufEvents($self, zl_div) : $self.removeClass('zl_img_switch').css('color', '').siblings('div').stop(true, true).slideUp(setting.foldingSpeed, setting.easingEffect).data(d_switch, d_off).end().parent('li').css('background-color', '')
                } else {
                    if (zl_div.data(d_switch) === d_off || !zl_div.data(d_switch)) {
                        fufEvents($self, zl_div)
                    }
                }
            })
        })
    }
})(jQuery, window, document);