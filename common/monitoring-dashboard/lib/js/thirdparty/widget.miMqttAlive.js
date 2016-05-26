(function()
{
	//Our RAG indicator styles
	freeboard.addStyle('.mimqtt-light', "border-radius:50%;width:22px;height:22px;border:2px solid #3d3d3d;margin-top:5px;float:left;background-color:#222;margin-right:10px;");
	freeboard.addStyle('.mimqtt-light.red', "background-color:#D90000;box-shadow: 0px 0px 15px #D90000;border-color:#FDF1DF;");
	freeboard.addStyle('.mimqtt-light.amber', "background-color:#E49B00;box-shadow: 0px 0px 15px #E49B00;border-color:#FDF1DF;");
	freeboard.addStyle('.mimqtt-light.green', "background-color:#00B60E;box-shadow: 0px 0px 15px #00B60E;border-color:#FDF1DF;");
	freeboard.addStyle('.mimqtt-text', "margin-top:10px;");
	
	var mimqttWidget = function (settings) {
        var self = this;
        var titleElement = $('<h2 class="section-title"></h2>');
        var stateElement = $('<div class="mimqtt-text"></div>');
        var indicatorElement = $('<div class="mimqtt-light"></div>');
        var currentSettings = settings;
		
		//store our calculated values in an object
		var stateObject = {"value": 0 };
		
		//array of our values: 0=Green, 2=Amber, 3=Red
		var stateArray = ["green", "amber", "red"];
        
	self.updateState = function() {        
                   var timestamp = window.mimqtt[currentSettings.url]["data"][currentSettings.topic]["timestamp"];
                   var now  = new Date().getTime();
                   if(timestamp + (currentSettings.warn_seconds*1000)>= now){
                      stateObject["status"] = "OK";
                      stateObject.value = 0;
                   }else if(timestamp + (currentSettings.error_seconds*1000)< now){
                      stateObject["status"] = "PROBLEM";
                      stateObject.value = 2;
                   }else{
                      stateObject["status"] = "LATE";
                      stateObject.value = 1;
                   }
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
            currentSettings.warn_seconds = parseInt(currentSettings.warn_seconds);
            currentSettings.error_seconds = parseInt(currentSettings.error_seconds);
            if(window.mimqtt === undefined){
               window.mimqtt = {};
            }
            if(window.mimqtt[currentSettings.url] === undefined){
               var client = mqtt.connect(currentSettings.url);
               client.on("message", function(topic, payload) {
                   //console.log(topic,payload.toString(),currentSettings);
                   var timestamp = new Date().getTime();
                   var latest = {timestamp: timestamp, payload: payload };
                   window.mimqtt[currentSettings.url]["data"][topic] = latest;
               });
               window.mimqtt[currentSettings.url] = {client: client, data: {}}
            }
            if(window.mimqtt[currentSettings.url]["data"][currentSettings.topic] === undefined){
                   var timestamp = new Date().getTime() - (currentSettings.warnSeconds * 1000);
                   var dummy = {timestamp: timestamp, payload: "No Messages" };
                   window.mimqtt[currentSettings.url]["data"][currentSettings.topic] = dummy;
                   window.mimqtt[currentSettings.url]["client"].subscribe(currentSettings.topic);
                   console.log("subscribed to ",currentSettings.topic,"on",currentSettings.url);
            }
            titleElement.html(newSettings.title);
            self.updateState();
        }

        this.onCalculatedValueChanged = function (settingName, newValue) {
            //whenever a calculated value changes, store them in the variable 'stateObject'
			stateObject[settingName] = newValue;
            self.updateState();
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
           refreshTimer = setInterval(function(){self.updateState();},5000);
        };
        createRefreshTimer();
    };

    freeboard.loadWidgetPlugin({
        type_name: "mimqttIndicator",
        display_name: "MI MQTT Alive Indicator",
        settings: [
            {
                name: "title",
                display_name: "Title",
                type: "text"
            },
            {
                name: "url",
                display_name: "MQTT Server URL",
                default_value: "http://mqtt.marine.ie",
                type: "text"
            },
            {
                name: "topic",
                display_name: "MQTT Topic",
                type: "text"
            },
            {
                name: "warn_seconds",
                display_name: "LATE if not updated Within ??? Seconds",
                default_value: "30",
                type: "text"
            },
            {
                name: "error_seconds",
                display_name: "ERROR if not updated Within ??? Seconds",
                default_value: "300",
                type: "text"
            },
            {
                name: "link",
                display_name: "Link To",
                default_value: "http://mqtt.marine.ie",
                type: "text"
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new mimqttWidget(settings));
        }
    });
}());
