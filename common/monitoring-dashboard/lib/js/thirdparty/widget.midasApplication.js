(function()
{
	//Our RAG indicator styles
	freeboard.addStyle('.midasApplication-light', "border-radius:50%;width:22px;height:22px;border:2px solid #3d3d3d;margin-top:5px;float:left;background-color:#222;margin-right:10px;");
	freeboard.addStyle('.midasApplication-light.red', "background-color:#D90000;box-shadow: 0px 0px 15px #D90000;border-color:#FDF1DF;");
	freeboard.addStyle('.midasApplication-light.amber', "background-color:#E49B00;box-shadow: 0px 0px 15px #E49B00;border-color:#FDF1DF;");
	freeboard.addStyle('.midasApplication-light.green', "background-color:#00B60E;box-shadow: 0px 0px 15px #00B60E;border-color:#FDF1DF;");
	freeboard.addStyle('.midasApplication-text', "margin-top:10px;");
	
	var midasApplicationWidget = function (settings) {
        var self = this;
        var titleElement = $('<h2 class="section-title"></h2>');
        var stateElement = $('<div class="midasApplication-text"></div>');
        var indicatorElement = $('<div class="midasApplication-light"></div>');
        var currentSettings = settings;
		
		//store our calculated values in an object
		var stateObject = {};
		
		//array of our values: 0=Green, 2=Amber, 3=Red
		var stateArray = ["green", "amber", "red"];
        
		function updateState() {         
                        var url = currentSettings.url;
                        var warning_timeout = parseInt(current_settings.warning_timeout);
                        warning_timeout = warning_timeout ? warning_timeout : 30;
                        var error_timeout = parseInt(current_settings.error_timeout);
                        error_timeout = error_timeout ? error_timeout : 30;
                      $.ajax({
                           url : url,
                           dataType: 'json',
                           success : function(data){
                             try {
                                 var status = "OK";
                                 stateObject.value=0;
                                 if(data.seconds_since_updated >= error_timeout){
                                     status = "PROBLEM";
                                     stateObject.value=2;
                                 }else if (data.seconds_since_updated >= warning_timeout){
                                     status = "LATE";
                                     stateObject.value=1;
                                 }
                                 stateObject["status"] = "<a title='"+JSON.stringify(data.message)+"' target='_blank' href='"+url+"'>"+status+"</a>";
                             }
                             catch(err) {
                                 stateObject["status"] = "<a title='error' target='_blank' href='"+url+"'>PROBLEM</a>";
                                 stateObject.value=2;
                             }
                          }
                      }).fail(function(){
                           stateObject["status"] = "<a title='problem fetching' target='_blank' href='"+url+"'>PROBLEM</a>";
                           stateObject.value= 2;
                         }
                       ).always(function(){
                           _updateState();
                         });  
                }
                function _updateState() {
		
			//Remove all classes from our indicator light
			indicatorElement
				.removeClass('red')
				.removeClass('amber')					
				.removeClass('green');
			
			var midasApplicationValue = _.isUndefined(stateObject.value) ? -1 : stateObject.value;			
			indicatorElement.addClass(stateArray[stateObject.value]);
			stateElement.html(stateObject.status);
		
        }

        this.render = function (element) {
            $(element).append(titleElement).append(indicatorElement).append(stateElement);			
        }		

        this.onSettingsChanged = function (newSettings) {
            currentSettings = newSettings;
            titleElement.html(newSettings.application_name);
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
        type_name: "midasApplicationIndicator",
        display_name: "MI DAS Application Indicator",
        settings: [
            {
                name: "application_name",
                display_name: "Application Name",
                type: "text"
            },
            {
                name: "url",
                display_name: "URL",
                type: "text"
            },
            {
                name: "warning_timeout",
                display_name: "Warning Timeout",
                default_value: "60",
                type: "text"
            },
            {
                name: "error_timeout",
                display_name: "Error Timeout",
                default_value: "300",
                type: "text"
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new midasApplicationWidget(settings));
        }
    });
}());
