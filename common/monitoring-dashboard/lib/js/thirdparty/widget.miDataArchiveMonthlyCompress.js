(function()
{
	//Our RAG indicator styles
	freeboard.addStyle('.midasmc-light', "border-radius:50%;width:22px;height:22px;border:2px solid #3d3d3d;margin-top:5px;float:left;background-color:#222;margin-right:10px;");
	freeboard.addStyle('.midasmc-light.red', "background-color:#D90000;box-shadow: 0px 0px 15px #D90000;border-color:#FDF1DF;");
	freeboard.addStyle('.midasmc-light.amber', "background-color:#E49B00;box-shadow: 0px 0px 15px #E49B00;border-color:#FDF1DF;");
	freeboard.addStyle('.midasmc-light.green', "background-color:#00B60E;box-shadow: 0px 0px 15px #00B60E;border-color:#FDF1DF;");
	freeboard.addStyle('.midasmc-text', "margin-top:10px;");
	
	var midasmcWidget = function (settings) {
        var self = this;
        var titleElement = $('<h2 class="section-title"></h2>');
        var stateElement = $('<div class="midasmc-text"></div>');
        var indicatorElement = $('<div class="midasmc-light"></div>');
        var currentSettings = settings;
		
		//store our calculated values in an object
		var stateObject = {"fails": 0};
		
		//array of our values: 0=Green, 2=Amber, 3=Red
		var stateArray = ["green", "amber", "red"];
        
		function updateState() {         
                        var dtype = currentSettings.device_type;
                        var device = currentSettings.device;
                        var base = "http://spiddal.marine.ie/data/";
                        var thirty_seven_days = 1000*60*60*24*37;
                        var d = new Date(new Date().getTime() - thirty_seven_days);
                        var year = d.getUTCFullYear();
                        var month = ("0"+(d.getUTCMonth()+1)).slice(-2);
                        var filename = device+"_"+year+month+".tgz";
                        var folder_url = base+dtype+"/"+device+"/";
                        var url = folder_url+filename;
                        stateObject.value = 1;
                      $.ajax({
                           url : url,
                           type : 'HEAD',
                          dataType: 'text/plain',
                           success : function(){
                             stateObject["status"] = "<a target='"+device+"' href='"+folder_url+"'>OK</a>";
                             stateObject.value=0;
                          }
                      }).fail(function(){
                           stateObject["status"] = "<a target='"+device+"' href='"+folder_url+"'>Missing "+filename+"</a>";
                           stateObject.value=2;
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
			
			var midasmcValue = _.isUndefined(stateObject.value) ? -1 : stateObject.value;			
			indicatorElement.addClass(stateArray[stateObject.value]);
			stateElement.html(stateObject.status);
		
        }

        this.render = function (element) {
            $(element).append(titleElement).append(indicatorElement).append(stateElement);			
        }		

        this.onSettingsChanged = function (newSettings) {
            currentSettings = newSettings;
            titleElement.html(newSettings.device_type+"/"+newSettings.device);
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
        type_name: "midasmcIndicator",
        display_name: "MI Monthly Compress Indicator",
		external_scripts: [
			"plugins/thirdparty/jquery.keyframes.min.js"
		],
        settings: [
            {
                name: "device_type",
                display_name: "Device Type",
                type: "text"
            },
            {
                name: "device",
                display_name: "Device",
                type: "text"
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new midasmcWidget(settings));
        }
    });
}());
