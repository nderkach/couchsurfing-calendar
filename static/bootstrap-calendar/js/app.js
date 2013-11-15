(function($) {

	"use strict";

	var options = {
		events_source: '/get',
		first_day: 1,
		view: 'month',
		tmpl_path: '/static/bootstrap-calendar/tmpls/',
		tmpl_cache: false,
		day: 'now',
		onAfterEventsLoad: function(events) {
			if(!events) {
				return;
			}
			var alist = $('#accepted');
			alist.html('');

			$.each(events, function(key, val) {
				console.log(val.class);
				if (val.class === "event-success") {
					$(document.createElement('li'))
						.html('<div style="max-height: 47px; padding-left: 5px;"><a class="pull-left event ' + val.class + '"</a><a href="' + val.url + '" target="_blank">' + val.title + '</a></div>')
						.appendTo(alist);
				}
			});

			var plist = $('#pending');
			plist.html('');

			$.each(events, function(key, val) {
				if (val.class === "event-warning") {
					$(document.createElement('li'))
						.html('<div style="max-height: 47px; padding-left: 5px;"><a class="pull-left event ' + val.class + '"</a><a href="' + val.url + '" target="_blank">' + val.title + '</a></div>')
						.appendTo(plist);
				}
			});

			document.getElementById('loading').style.visibility = "hidden";
		},
		onAfterViewLoad: function(view) {
			$('.page-header h3').text(this.getTitle());
			$('.btn-group button').removeClass('active');
			$('button[data-calendar-view="' + view + '"]').addClass('active');
			$('#cal-view').animate({ opacity: 1.0 });
		},
		onBeforeEventsLoad: function(next) {
			document.getElementById('loading').style.visibility = "visible";
			next();
		},
		classes: {
			months: {
				general: 'label'
			}
		}
	};

	var calendar = $('#calendar').calendar(options);

	$('.btn-group button[data-calendar-nav]').each(function() {
		var $this = $(this);
		$this.click(function() {
			calendar.navigate($this.data('calendar-nav'));
		});
	});

	$('.btn-group button[data-calendar-view]').each(function() {
		var $this = $(this);
		$this.click(function() {
			calendar.view($this.data('calendar-view'));
		});
	});

	$('#first_day').change(function(){
		var value = $(this).val();
		value = value.length ? parseInt(value) : null;
		calendar.setOptions({first_day: value});
		calendar.view();
	});

	$('#language').change(function(){
		calendar.setLanguage($(this).val());
		calendar.view();
	});

	$('#events-in-modal').change(function(){
		var val = $(this).is(':checked') ? $(this).val() : null;
		calendar.setOptions({modal: val});
	});
	$('#events-modal .modal-header, #events-modal .modal-footer').click(function(e){
		e.preventDefault();
		e.stopPropagation();
	});
}(jQuery));