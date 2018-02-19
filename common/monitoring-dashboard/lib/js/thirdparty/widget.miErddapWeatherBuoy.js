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
                function getErddapUrl(station_id,minutes){
                      var base = "http://erddap.marine.ie/erddap/tabledap/IWBNetwork.json?longitude,latitude,time,station_id&time>=";
                      var time = new Date(new Date().getTime() - (minutes*60*1000)).toISOString();
                      var url = base+time+"&station_id=%22"+encodeURIComponent(station_id)+"%22";
                      return url;
                }
                function updateStateFromErddap(station_id,state,urls,prev_url){
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
                                return updateStateFromErddap(station_id,state+1,urls,url);
                             }else{
                                 var ok = state == 0?"OK":"LATE";
                                 stateObject["status"] = "<a target='"+station_id+"' href='"+url+"'>"+ok+"</a>";
                                 stateObject.value=state;
                                _updateState();
                             }
                          }
                      }).fail(function(){
                             updateStateFromErddap(station_id,state+1,urls,url);
                      });
                   }else{
                          stateObject["status"] = "<a target='"+station_id+"' href='"+prev_url+"'>PROBLEM</a>";
                          stateObject.value = state;
                         _updateState();
                   }
                }
        
		function updateState() {         
                    var station_id = currentSettings.station_id;
                    var warn_minutes = parseInt(currentSettings.warn_minutes);
                    var error_minutes = parseInt(currentSettings.error_minutes);
                    var urls = [getErddapUrl(station_id,warn_minutes),getErddapUrl(station_id,error_minutes)];
                    updateStateFromErddap(station_id,0,urls,urls[0]);
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
            titleElement.html(newSettings.station_id);
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
        type_name: "weatherBuoyIndicator",
        display_name: "Erddap Weather Buoy Indicator",
		external_scripts: [
			"plugins/thirdparty/jquery.keyframes.min.js"
		],
        settings: [
            {
                name: "station_id",
                display_name: "Station ID",
                type: "text"
            },
            {
                name: "warn_minutes",
                display_name: "LATE if not updated Within  Minutes",
                default_value: "60",
                type: "text"
            },
            {
                name: "error_minutes",
                display_name: "ERROR if not updated Within Minutes",
                default_value: "120",
                type: "text"
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new midasWidget(settings));
        }
    });
}());
