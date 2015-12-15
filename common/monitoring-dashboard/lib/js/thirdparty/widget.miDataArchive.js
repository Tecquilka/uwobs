(function()
{
	//Our RAG indicator styles
	freeboard.addStyle('.midas-light', "border-radius:50%;width:22px;height:22px;border:2px solid #3d3d3d;margin-top:5px;float:left;background-color:#222;margin-right:10px;");
	freeboard.addStyle('.midas-light.red', "background-color:#D90000;box-shadow: 0px 0px 15px #D90000;border-color:#FDF1DF;");
	freeboard.addStyle('.midas-light.amber', "background-color:#E49B00;box-shadow: 0px 0px 15px #E49B00;border-color:#FDF1DF;");
	freeboard.addStyle('.midas-light.green', "background-color:#00B60E;box-shadow: 0px 0px 15px #00B60E;border-color:#FDF1DF;");
	freeboard.addStyle('.midas-text', "margin-top:10px;");
	
	var midasWidget = function (settings) {
        var self = this;
        var titleElement = $('<h2 class="section-title"></h2>');
        var stateElement = $('<div class="midas-text"></div>');
        var indicatorElement = $('<div class="midas-light"></div>');
        var currentSettings = settings;
		
		//store our calculated values in an object
		var stateObject = {"fails": 0};
		
		//array of our values: 0=Green, 2=Amber, 3=Red
		var stateArray = ["green", "amber", "red"];
                function getPossibleUrls(dtype,device,ext,quantity){
                   var urls = [];
                   for(var i=quantity; i>0; i--){
                      var base = "http://spiddal.marine.ie/data/";
                      var d = new Date(new Date().getTime() - (i*60*1000));
                      var year = d.getUTCFullYear();
                      var month = ("0"+(d.getUTCMonth()+1)).slice(-2);
                      var day = ("0"+d.getUTCDate()).slice(-2);
                      var hour = ("0"+d.getUTCHours()).slice(-2);
                      var minute = ("0"+d.getUTCMinutes()).slice(-2);
                      var filename = device+"_"+year+month+day+"_"+hour+minute+ext;
                      var folder_url = base+dtype+"/"+device+"/"+year+"/"+month+"/"+day+"/";
                      var url = folder_url+filename;
                      urls.push(url);
                   }
                   return urls;
                }
                function verifyOneUrl(device,urls,prev_url){
                   stateObject.value = 1;
                   if(urls.length > 0){
                      var url = urls.shift();
                      $.ajax({
                           url : url,
                           type : 'HEAD',
                          dataType: 'text/plain',
                           success : function(){
                             stateObject["status"] = "<a target='"+device+"' href='"+url+"/..'>OK</a>";
                             stateObject["fails"] = 0;
                             stateObject.value=0;
                            _updateState();
                          }
                      }).fail(function(){
                             return verifyOneUrl(device,urls,url);
                      });
                   }else{
                          stateObject["status"] = "<a target='"+device+"' href='"+prev_url+"/..'>PROBLEM</a>";
                          stateObject["fails"] += 1;
                          stateObject.value= stateObject.fails>=5?2:1;
                         _updateState();
                   }
                }
        
		function updateState() {         
                        var dtype = currentSettings.device_type;
                        var device = currentSettings.device;
                        var ext = currentSettings.ext;
                        var quantity = parseInt(currentSettings.within_minutes);
                        quantity = quantity? quantity: 5;
                        var urls = getPossibleUrls(dtype,device,ext,quantity);
                        verifyOneUrl(device,urls);
                }
                function _updateState() {
		
			//Remove all classes from our indicator light
			indicatorElement
				.removeClass('red')
				.removeClass('amber')					
				.removeClass('green');
			
			var midasValue = _.isUndefined(stateObject.value) ? -1 : stateObject.value;			
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
        type_name: "midasIndicator",
        display_name: "MI Archive Indicator",
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
            },
            {
                name: "ext",
                display_name: "File Extension",
                type: "text"
            },
            {
                name: "within_minutes",
                display_name: "Updated Within Minutes",
                default_value: "5",
                type: "text"
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new midasWidget(settings));
        }
    });
}());
