(function()
{
	//Our RAG indicator styles
	freeboard.addStyle('.ocean-light', "border-radius:50%;width:22px;height:22px;border:2px solid #3d3d3d;margin-top:5px;float:left;background-color:#222;margin-right:10px;");
	freeboard.addStyle('.ocean-light.red', "background-color:#D90000;box-shadow: 0px 0px 15px #D90000;border-color:#FDF1DF;");
	freeboard.addStyle('.ocean-light.amber', "background-color:#E49B00;box-shadow: 0px 0px 15px #E49B00;border-color:#FDF1DF;");
	freeboard.addStyle('.ocean-light.green', "background-color:#00B60E;box-shadow: 0px 0px 15px #00B60E;border-color:#FDF1DF;");
	freeboard.addStyle('.ocean-text', "margin-top:10px;");
	
	var oceanWidget = function (settings) {
        var self = this;
        var titleElement = $('<h2 class="section-title"></h2>');
        var stateElement = $('<div class="ocean-text"></div>');
        var indicatorElement = $('<div class="ocean-light"></div>');
        var currentSettings = settings;
		
		//store our calculated values in an object
		var stateObject = {"fails": 0};
		
		//array of our values: 0=Green, 2=Amber, 3=Red
		var stateArray = ["green", "amber", "red"];
                function getDatedUrl(url,days){
                      var time = new Date(new Date().getTime() + (days*24*60*60*1000)).toISOString().substring(0,10);
                      return url.replace(/CHECKDATE/g,time);
                }
                function updateStateFromErddap(state,urls,prev_url,hours){
                   stateObject.value = 1;
                   if(urls.length > 0){
                      var url = urls.shift();
                      $.ajax({
                           url : url,
                           //dataType:"jsonp",
                           //jsonp:".jsonp",
                           cache: true,
                           success : function(data){
                             if(data.table.rows.length == 0){
                                return updateStateFromErddap(state+1,urls,url,hours);
                             }else{
                                 var ok = state == 0?"OK":"LATE";
                                 stateObject["status"] = "<a target='_blank' href='"+url.replace("json","htmlTable")+"'>"+ok+"</a>";
                                 stateObject.value=state;
                                _updateState();
                             }
                          }
                      }).fail(function(){
                             if(state>0&&hours>0&&new Date().getHours()<hours){
                                 state = state-1;
                             }
                             updateStateFromErddap(state+1,urls,url,hours);
                      });
                   }else{
                          stateObject["status"] = "<a target='_blank' href='"+prev_url.replace("json","htmlTable")+"'>PROBLEM</a>";
                          stateObject.value = state;
                         _updateState();
                   }
                }
        
		function updateState() {         
                    var url = currentSettings.url;
                    var hours = parseInt(currentSettings.hours);
                    var warn_days = parseInt(currentSettings.warn_days);
                    var error_days = parseInt(currentSettings.error_days);
                    var urls = [getDatedUrl(url,warn_days),
                                getDatedUrl(url,error_days)];
                    updateStateFromErddap(0,urls,urls[0],hours);
                }
                function _updateState() {
		
			//Remove all classes from our indicator light
			indicatorElement
				.removeClass('red')
				.removeClass('amber')					
				.removeClass('green');
			
			var oceanValue = _.isUndefined(stateObject.value) ? -1 : stateObject.value;			
			indicatorElement.addClass(stateArray[stateObject.value]);
			stateElement.html(stateObject.status);
		
        }

        this.render = function (element) {
            $(element).append(titleElement).append(indicatorElement).append(stateElement);			
        }		

        this.onSettingsChanged = function (newSettings) {
            currentSettings = newSettings;
            titleElement.html(newSettings.title);
            updateState();
        }

        this.onCalculatedValueChanged = function (settingName, newValue) {
            //whenever a calculated value changes, store them in the variable 'stateObject'
			stateObject[settingName] = newValue;
            updateState();
        }

        this.onDispose = function () {
        }

        this.getHeight = function () {
            return 1;
        }

        this.onSettingsChanged(settings);
        var refreshTimer;
        var createRefreshTimer = function(){
           if(refreshTimer){
              clearInterval(refreshTimer);
           }
           refreshTimer = setInterval(function(){updateState();},60000);
        };
        createRefreshTimer();
    };

    freeboard.loadWidgetPlugin({
        type_name: "forecastIndicator",
        display_name: "Erddap Forecast Indicator",
		external_scripts: [
			"plugins/thirdparty/jquery.keyframes.min.js"
		],
        settings: [
            {
                name: "title",
                display_name: "Widget Title",
                type: "text"
            },
            {
                name: "url",
                display_name: "JSON URL (replace date with CHECKDATE)",
                type: "text"
            },
            {
                name: "warn_days",
                display_name: "WARN if no data X days into future",
                default_value: "5",
                type: "text"
            },
            {
                name: "error_days",
                display_name: "ERROR if no data Y days into future",
                default_value: "4",
                type: "text"
            },
            {
                name: "hours",
                type: "option",
                default_value: "0",
                display_name: "Allowable delay",
                options : [
                   { name: "None", value: "0" },
                   { name: "6am", value: "6" },
                   { name: "9am", value: "9" },
                   { name: "12 noon", value: "12" },
                   { name: "3pm", value: "15" },
                   { name: "6pm", value: "18" }
                ]
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new oceanWidget(settings));
        }
    });
}());
