/**
 * @author Semika Siriwardana(semika.siriwardana@gmail.com)
 */
function ChatWindow(config) {
	var _self = this;
    this.chatId = config.chatId;
    this.maxMessageId = config.maxMessageId;
    this.name = config.name;
    this.peer = config.peer;
    this.title = config.title;
    this.source = config.source;
    this._windowWidth  = config.width;
    this._windowHeight = config.height;
    this.index = config.index;
    var hidden = false;

    this.getChatId = function () {
        return this.chatId;
    };

    this.getMaxMessageId = function() {
        return this.maxMessageId;
    };

    this.getWindowLeftPosition = function() {
    	return this.index*this._windowWidth;
    },
    
    this.getPeerUserName = function() {
    	return this.peer;
    };
    
    this.getLoginUserName = function() {
    	return this.name;
    };
    
    this.getMessageContainerID = function() {
    	return this.getLoginUserName() + "_" + this.getPeerUserName();
    };
    
    this.getTextInputID = function() {
    	return this.getLoginUserName() + "_" + this.getPeerUserName() + "_chatInput";
    };
    
    this.getWindowID = function() {
    	return this.getLoginUserName() + "_" + this.getPeerUserName() + "_window";
    };
    
    this.hide = function(_self) {
        hidden = true;
        jq("#" + _self.getWindowID()).css("display", "none");
    };
    
    this.show = function() {
        hidden = false;
    	jq("#" + this.getWindowID()).css("display", "block");
    };
    
    /**
     * Returns whether the chat window is currently visible or not
     */
    this.isVisible = function() {
    	return jq("#" + this.getWindowID()).css("display") == "none"?false:true;
    };
    
    this.addOnClickListener = function(el, fnHandler, context) {
        jq(el).bind("click", context, function(evt) {
            if(context != undefined) {
                fnHandler(context);
            } else {
                fnHandler();
            }
            return false;
        });
    };
    this.appendText = function(text) {
        var chatContainer = jq("#" + this.getMessageContainerID());
        var sb = [];
        sb[sb.length] = text;
        chatContainer.append(sb.join(""));
        chatContainer[0].scrollTop = chatContainer[0].scrollHeight - chatContainer.outerHeight();
    }
    this.appendMessage = function(fromUser, text) {
    	
    	var userNameCssClass    = "toUserName";
    	var textMessageCssClass = "toMessage";
    	
    	if( fromUser!=='Agent' ) {
            fromUser = 'Customer';
        }
    	var chatContainer = jq("#" + this.getMessageContainerID());
    	var sb = [];
    	sb[sb.length] = '<span class="' + userNameCssClass + '">' + fromUser + ':</span>';
    	sb[sb.length] = '<span class="' + textMessageCssClass + '" style="margin-left:4px;">' + text + '</span><br/>';
    	chatContainer.append(sb.join(""));  
    	chatContainer[0].scrollTop = chatContainer[0].scrollHeight - chatContainer.outerHeight();
    };
    this.update = function(messages) {
        if ( messages ) {
            for(var i=0;i<messages.length;i++) {
                if ( messages[i].id>this.maxMessageId ) {
                    if ( hidden ) {
                        var snd = new Audio('/static/admin/mp3/incoming_msg.ogg');
                        snd.load();
                        snd.play();
                    }
                    this.show();
                    this.maxMessageId = messages[i].id;
                    if ( messages[i].source=='backoffice' ) {
                        // from backoffice
                        this.appendMessage('Agent', messages[i].content);
                    } else {
                        this.appendMessage('Customer', messages[i].content);
                    }
                }
            }
        }
    }
    
    this.focusTextInput = function() {
    	jq("#" + this.getTextInputID()).focus();
    },
    
    this.getWindowBody = function() {
    	
    	var bodyDIV = document.createElement("div");
    	bodyDIV.setAttribute("id", this.getMessageContainerID()); 
    	bodyDIV.style.width     = this._windowWidth + "px";
    	bodyDIV.style.height    = (this._windowHeight-25-23)+"px";
    	bodyDIV.style.position  = 'absolute';
    	bodyDIV.style.left      = 0;
    	bodyDIV.style.bottom    = "23px";
    	bodyDIV.style.overflowY = 'auto';
        bodyDIV.style.paddingLeft = '3px';
        bodyDIV.style.paddingRight = '3px';
    	return bodyDIV;
    };
    
    this.getWindowFooter = function() {
    	
    	var footerDIV = document.createElement("div");
    	footerDIV.style.width  = this._windowWidth + "px";
    	footerDIV.style.height = "23px";
    	footerDIV.style.position = 'absolute';
    	footerDIV.style.left     = 0;
    	footerDIV.style.bottom   = 0;
    	
    	//create text input
    	var textInput = document.createElement("input");
    	textInput.setAttribute("id", this.getTextInputID());
    	textInput.setAttribute("type", "text");
    	textInput.setAttribute("name", "chatInput");
    	textInput.setAttribute("class", "chatInput");
    	
    	jq(textInput).attr('autocomplete', 'off');
        jq(textInput).keyup(function(e) {
            if (e.keyCode == 13) {
                var jsonData = null;
                try {
                    jsonData = JSON.stringify({peer:_self.getPeerUserName(), message:jq(textInput).val(), chatId:_self.chatId, source:_self.source});
                } catch(e) {
                    jsonData = jq.toJSON({peer:_self.getPeerUserName(), message:jq(textInput).val(), chatId:_self.chatId, source:_self.source});
                }
                jq.ajax({
                    type: "POST",
                    url: "/admin/rest/chat/send",
                    contentType : 'application/json',
                    data: jsonData
                });
            	jq(textInput).val('');
            	jq(textInput).focus();
            }
        });
        
    	footerDIV.appendChild(textInput);
    	
    	return footerDIV;
    };
    
    this.getWindowHeader = function() {
    	
    	var headerDIV = document.createElement("div");
    	headerDIV.style.width  = this._windowWidth + "px";
    	headerDIV.style.height = "25px";
        headerDIV.style.backgroundColor = '#4D68A2';
        headerDIV.style.position = 'relative';
    	headerDIV.style.top      = 0;
    	headerDIV.style.left     = 0;
        headerDIV.style.fontFamily="Liberation Sans,Helvetica,Arial,sans-serif,STIXGeneral,Asana Math,Arial Unicode MS,Lucida Grande";
    	var textUserName = document.createElement("span");
    	textUserName.setAttribute("class", "windowTitle");
    	textUserName.innerHTML = '<img src="/static/admin/img/chat.gif" style="margin-right:4px;"/>'+this.title;


    	var textClose = document.createElement("span");
    	textClose.setAttribute("class", "windowClose");
    	textClose.innerHTML = "X";
    	this.addOnClickListener(textClose, this.hide, this);
    	
    	headerDIV.appendChild(textUserName);
    	headerDIV.appendChild(textClose);
    	
    	return headerDIV;
    };
    
    this.getWindowHTML = function() {
    	
    	var windowDIV = document.createElement("div");
    	windowDIV.setAttribute("id", this.getWindowID());
    	windowDIV.style.width  = this._windowWidth + "px"; 
    	windowDIV.style.height = this._windowHeight +"px";
    	windowDIV.style.backgroundColor = '#FFFFFF'; 
    	windowDIV.style.position = 'absolute';
    	windowDIV.style.bottom   = 0;
    	windowDIV.style.right    = this.getWindowLeftPosition() + "px"; 
    	windowDIV.style.zIndex   = 100;
    	windowDIV.style.border   = '1px solid #4D68A2';
    	
    	windowDIV.appendChild(this.getWindowHeader()); 
    	windowDIV.appendChild(this.getWindowBody());
    	windowDIV.appendChild(this.getWindowFooter()); 
    	
    	return windowDIV;
    };
    
    this.initWindow = function() {
    	var body = document.getElementsByTagName('body')[0];
    	body.appendChild(this.getWindowHTML()); 
    	//focus text input just after opening window
    	this.focusTextInput();
    };
}