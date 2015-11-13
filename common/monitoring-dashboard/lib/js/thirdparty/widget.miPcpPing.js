(function()
{
	//Our RAG indicator styles
	freeboard.addStyle('.mipcp-light', "border-radius:50%;width:22px;height:22px;border:2px solid #3d3d3d;margin-top:5px;float:left;background-color:#222;margin-right:10px;");
	freeboard.addStyle('.mipcp-light.red', "background-color:#D90000;box-shadow: 0px 0px 15px #D90000;border-color:#FDF1DF;");
	freeboard.addStyle('.mipcp-light.amber', "background-color:#E49B00;box-shadow: 0px 0px 15px #E49B00;border-color:#FDF1DF;");
	freeboard.addStyle('.mipcp-light.green', "background-color:#00B60E;box-shadow: 0px 0px 15px #00B60E;border-color:#FDF1DF;");
	freeboard.addStyle('.mipcp-text', "margin-top:10px;");
	
	var mipcpWidget = function (settings) {
        var self = this;
        var titleElement = $('<h2 class="section-title"></h2>');
        var stateElement = $('<div class="mipcp-text"></div>');
        var indicatorElement = $('<div class="mipcp-light"></div>');
        var currentSettings = settings;
		
		//store our calculated values in an object
		var stateObject = {"fails": 0, "context": undefined ,"base_url": "http://example.pcp.dm.marine.ie/"};
		
		//array of our values: 0=Green, 2=Amber, 3=Red
		var stateArray = ["green", "amber", "red"];
        
		function updateState() {        
                    if (_.isUndefined(stateObject.context)){
                      $.ajax({
                           url : stateObject.base_url+"pmapi/context?hostspec=localhost&polltimeout=600",
                          dataType: 'json',
                           success : function(data){
                             stateObject["context"] = data["context"];
                             updateState()
                          }
                      }).fail(function(){
                           stateObject["status"] = "PROBLEM";
                           stateObject["fails"] += 1;
                           stateObject.value= stateObject.fails>=5?2:1;
                           _updateState();
                         }
                       );  
                    }else{
                      $.ajax({
                          url : stateObject.base_url+"pmapi/"+stateObject.context+"/_fetch?names=filesys.capacity,filesys.used,filesys.free",
                          dataType: 'json',
                           success : function(data){
                             // could improve this by looking at some key indicators like disk space...
                             stateObject["status"] = "OK";
                             stateObject.value = 0;
                             _updateState()
                          }
                      }).fail(function(){
                           stateObject["status"] = "PROBLEM";
                           stateObject["fails"] += 1;
                           stateObject.value= stateObject.fails>=5?2:1;
                           _updateState();
                         }
                       );  
                    }
                }
                function _updateState() {
		
			//Remove all classes from our indicator light
			indicatorElement
				.removeClass('red')
				.removeClass('amber')					
				.removeClass('green');
			
			var mipcpValue = _.isUndefined(stateObject.value) ? -1 : stateObject.value;			
			indicatorElement.addClass(stateArray[stateObject.value]);
                        var link = '<a target="vector_'+currentSettings.hostname
                                  +'" href="http://vector.sysadmin.dm.marine.ie/#/?host='+currentSettings.hostname
                                  +'.pcp.dm.marine.ie&hostspec=localhost">'+stateObject.status+'</a>';
			stateElement.html(link);
		
        }

        this.render = function (element) {
            $(element).append(titleElement).append(indicatorElement).append(stateElement);			
        }		

        this.onSettingsChanged = function (newSettings) {
            currentSettings = newSettings;
            titleElement.html(newSettings.hostname);
            stateObject.base_url="http://"+newSettings.hostname+".pcp.dm.marine.ie/";
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
        type_name: "mipcpIndicator",
        display_name: "MI PCP Server Alive Indicator",
        settings: [
            {
                name: "hostname",
                display_name: "Hostname",
                type: "text"
            }
        ],
        newInstance: function (settings, newInstanceCallback) {
            newInstanceCallback(new mipcpWidget(settings));
        }
    });
}());
