(function()
{
	//Our RAG indicator styles
	freeboard.addStyle('.micch-light', "border-radius:50%;width:22px;height:22px;border:2px solid #3d3d3d;margin-top:5px;float:left;background-color:#222;margin-right:10px;");
	freeboard.addStyle('.micch-light.red', "background-color:#D90000;box-shadow: 0px 0px 15px #D90000;border-color:#FDF1DF;");
	freeboard.addStyle('.micch-light.amber', "background-color:#E49B00;box-shadow: 0px 0px 15px #E49B00;border-color:#FDF1DF;");
	freeboard.addStyle('.micch-light.green', "background-color:#00B60E;box-shadow: 0px 0px 15px #00B60E;border-color:#FDF1DF;");
	freeboard.addStyle('.micch-text', "margin-top:10px;");
	
	var micchWidget = function (settings) {
        var self = this;
        var titleElement = $('<h2 class="section-title"></h2>');
        var stateElement = $('<div class="micch-text"></div>');
        var indicatorElement = $('<div class="micch-light"></div>');
        var currentSettings = settings;
		
		//store our calculated values in an object
		var stateObject = {"value": 0, "data": "x" };
		
		//array of our values: 0=Green, 2=Amber, 3=Red
		var stateArray = ["green", "amber", "red"];
        
		function updateState() {        
                      $.ajax({
                          url : current_settings.url,
                          dataType: 'text',
                           success : function(data){
                             if( data == stateObject.data){
                               stateObject["status"] = "PROBLEM";
                               stateObject.value = stateObject.value == 0?1:2;
                             }else{
                               stateObject["status"] = "OK";
                               stateObject.value = 0;
                             }
                             _updateState()
                          }
                      }).fail(function(){
                           delete stateObject["context"];
                           stateObject["status"] = "PROBLEM";
                           stateObject.value = stateObject.value == 0?1:2;
                           _updateState();
                         }
                       );  
                }
                function _updateState() {
		
			//Remove all classes from our indicator light
			indicatorElement
				.removeClass('red')
				.removeClass('amber')					
				.removeClass('green');
			
			indicatorElement.addClass(stateArray[stateObject.value]);
                        var link = '<a target="_blank'
                                  +'" href="'+currentSettings.link
                                  +'">'+stateObject.status+'</a>';
			stateElement.html(link);
		
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
           refreshTimer = setInterval(function(){updateState();},15000);
        };
        createRefreshTimer();
    };

    freeboard.loadWidgetPlugin({
        type_name: "micchIndicator",
        display_name: "MI Content Changing Indicator",
        settings: [
            {
                name: "title",
                display_name: "Title",
                type: "text"
            },
            {
                name: "url",
                display_name: "URL",
                type: "text"
            },
            {
                name: "link",
                display_name: "Link To",
                type: "text"
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new micchWidget(settings));
        }
    });
}());
