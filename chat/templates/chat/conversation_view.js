"use strict";

  // django stuff
  </script>
  {{ conversation_messages|json_script:'conversation-messages' }}
  <script>

  let dConversationMessages = document.querySelector('#conversation-messages').textContent;
  let dConversationPk = Number('{{ conversation.pk }}');
  let dAllMessagesLoadedFromDb = '{{ all_messages_loaded_from_db }}' === 'True';
  let dUserUsername = '{{ user.username }}';
  let dUserPk = Number('{{ user.pk }}');
  let dUserIsStaff = '{{ user.is_staff }}' === 'True';
  let dLastReadMessagePk = Number('{{ last_read_message_pk }}');
  let dUserTimezoneOffset = Number('{{ user.profile.get_timezone_offset }}');
  let dUserTimezoneAbbreviation = '{{ user.profile.get_timezone_abbreviation }}';
  let dUserTimezoneName = '{{ user.profile.timezone.zone }}'

  // hide non-js form
  document.querySelector('#non-js-form').style['display'] = 'none';

let app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    optionsMenuShow: false,
    statusMessage: '',
    statusMessageTimeout: undefined,

    conversationPk: dConversationPk,

    userUsername: dUserUsername,
    userPk: dUserPk,
    userTimezoneAbbreviation: dUserTimezoneAbbreviation,
    userTimezoneName: dUserTimezoneName,
    userTimezoneOffset: dUserTimezoneOffset,
    userIsStaff: dUserIsStaff,
    userBackgroundColors: {},

    messages: JSON.parse(dConversationMessages),
    allMessagesFetched: false,
    allMessagesLoadedFromDb: dAllMessagesLoadedFromDb,
    lastReadMessagePk: dLastReadMessagePk,
    messageDisplayCount: 20,
    messageInputText: '',
    messageBeingEdited: undefined,
    messageUpdateText: '',

  },
  computed: {
    allMessagesShown() {
      return this.allMessagesFetched || this.allMessagesLoadedFromDb;
    },
  },
  created() {
    this.messagesGet = _.debounce(this.messagesGet, 400, {
      leading: true,
      trailing: false
    })
  },
  mounted() {
    
    // scroll to bottom of chatList
    this.$nextTick(() => {
      this.scrollToBottom(smooth=false);
    })

    // hide status messages after 5 seconds
    if (document.querySelector('#info-message-container')) {
      setTimeout(() => {
        document.querySelector('#info-message-container').classList.add('make-transparent');
        setTimeout(() => {
          document.querySelector('#info-message-container').classList.add('hide');
        }, 1000)
      }, 2000)
    }

    // when scrolled to top of chatList, load 10 more messages
    var chatList = document.querySelector('.chat-list');
    chatList.addEventListener('scroll', (e) => {
      if (chatList.scrollTop === 0) {
        this.messagesGetMore();
        this.$nextTick(() => {
          chatList.scrollTop = 1;
        })
      }
    })

    // poll for new messages every 5 seconds
    // setInterval(() => {this.messagesGet();}, 5000);
    
  },
  methods: {
    // date logic
    zeroPadder(num, minLength=2) {
      // get the minimum length of the result
      let sliceLength = minLength;
      let numLength = String(num).length;
      if (numLength > minLength) {sliceLength = numLength;}

      // create a string of zeroes
      let zeroString = '';
      for (let i = 0; i < sliceLength; i++) {zeroString += '0'}

      // return a string that is at least as long as minLength
      return (zeroString + String(num)).slice(numLength);
    },
    dateLocalize(dateObj, offset=0) {
      return new Date(dateObj.getTime() + this.userTimezoneOffset);
    },
    dateFormat(dateString, convertTo) {
      // convert to local time
      let dateObj = new Date(dateString);
      dateObj = this.dateLocalize(dateObj);
        if (convertTo === 'date') {
          return dateObj.toDateString();
        }
        else if (convertTo === 'hours') {
          let hours = dateObj.getHours();
          return this.zeroPadder(hours);
        }
        else if (convertTo === 'minutes') {
          let minutes = dateObj.getMinutes();
          return this.zeroPadder(minutes);
        }
    },
    checkIfIsNewDay(message) {
      // edge case
      let messageIndex = this.messageGetIndexFromPk(message.pk);
      if (messageIndex === this.messages.length-1) {return true;}

      if(messageIndex > 0) {
        let currentMessageDate = new Date(message.created_at);
        let previousMessageDate = new Date(this.messages[messageIndex+1].created_at);

        if (currentMessageDate.getYear() >= previousMessageDate.getYear() && +
            currentMessageDate.getMonth() >= previousMessageDate.getMonth() && + 
            currentMessageDate.getDay() > previousMessageDate.getDay()) {
          return true;
        }
        else {
          return false;
        }
      }
    },
    checkIfIsNewUser(message) {
      // edge case
      let messageIndex = this.messageGetIndexFromPk(message.pk);
      if (messageIndex === this.messages.length-1) {return true;}

      if(messageIndex >= 0) {
        let currentMessageUser = message.sender_username;
        let previousMessageUser = this.messages[messageIndex+1].sender_username;

        if (currentMessageUser !== previousMessageUser) {
          return true;

        }
        else {
          return false;
        }
      }
    },
    // ui methods
    elFlicker(el, flickerColor='#99f', startAfter=20, stopAfter=360) {
      let originalColor = el.style.backgroundColor;
      setTimeout(() => {
        el.style.backgroundColor = flickerColor;
      }, startAfter)
      setTimeout(() => {
        el.style.backgroundColor = originalColor;
      }, stopAfter)
    },
    messageElContentClass: function (message) {
      return {
        'cursor-url': this.userCanEdit(message),
        'item-current-user': this.userIsSender(message),
        'item-other-user': !this.userIsSender(message),
      }
    },
    messageElContentStyle: function (message) {
      return {
        'background-color': this.messageElBackgroundColorGet(message.sender_username),
        'box-shadow': message.pk === this.lastReadMessagePk ? '0 0 10px red' : '0 0 10px black'
      }
    },
    messageElBackgroundColorGet(username) {
      // if user's background color already calculated, use it
      if (Object.keys(this.userBackgroundColors).indexOf(username) !== -1) {
        return this.userBackgroundColors[username]
      }
      let maxValue = 255 - 16;
      let minValue = 128 + 32;
      let result = '';
      for (let i = 1; i <= 3; i++) {
        let seed = new Math.seedrandom(username.substr(username.length - i, username.length - i+1))();
        let thisResult = maxValue - Math.floor(seed * maxValue);
        result += thisResult.toString(16);
      }
      result = '#' + result;
      this.userBackgroundColors[username] = result;
      return result;
    },
    menuToggle() {
      this.optionsMenuShow = !this.optionsMenuShow;
    },
    displayStatusMessage(message, timeout=3000) {
      this.statusMessage = message;
      clearTimeout(this.statusMessageTimeout);
      this.statusMessageTimeout = setTimeout(() => {
        this.statusMessage = '';
      }, timeout)
    },
    getDistanceToBottom() {
      let el = this.$refs.chatList;
      let elementTotalHeight = el.scrollHeight;
      let elementVisibleHeight = el.clientHeight;
      let elementScrollHeight = el.scrollHeight - el.clientHeight;
      return elementScrollHeight;
    },
    isScrolledToBottom() {
      let el = this.$refs.chatList;
      if (el.scrollTop >= this.getDistanceToBottom() - 100) {
        return true;
      } else {
        return false;
      }
    },
    scrollToBottom(smooth=true) {
      this.$nextTick(() => {
        this.$refs.chatList.scrollTo({
          top: this.getDistanceToBottom(),
          behavior: smooth ? 'smooth' : 'auto'
        })
      })
    },
    // conversation logic
    userIsSender: function (message) {
      if (message.sender === this.userPk) {
        return true;
      } else return false;
    },
    userCanEdit: function (message) {
      if (this.userIsStaff) {
        return true;
      }
      else if (this.userPk === message.sender) {
        return true;
      }
      else {
        return false;
      }
    },
    messageGetIndexFromPk(messagePk) {
      /* for loop */
      // let pkList = [];
      // for (let i = 0; i < this.messages.length; i++) {
      // pkList.push(this.messages[i].pk)
      // }

      /* map */
      // let pkList = this.messages.map(x => x.pk);
      // let index = pkList.indexOf(messagePk)

      /* findIndex */
      return this.messages.findIndex(x => x.pk === messagePk);
    },
    messageGetByPk(messagePk) {
      return this.messages[this.messageGetIndexFromPk(messagePk)];
    },
    messageRemoveFromList(messagePk) {
      let index = this.messageGetIndexFromPk(messagePk);

      // shrink the deleted message along the y-axis
      let messageEl = eval('this.$refs.message' + messagePk)[0];

      // if the message is undefined, that means it has already been removed
      if (messageEl === undefined) {
        return false;
      }

      let messageElHeight = messageEl.offsetHeight;
      messageEl.style.transform = 'scale(1, 0)';
      messageEl.style.marginBottom = `-${messageEl.offsetHeight}px`
      this.messageUpdatePanelSelect(0);

    },
    messageUpdatePanelSelect: function (messagePk) {
      if (!messagePk) {
        this.messageBeingEdited = undefined;
        this.messageUpdateText = '';
        return false
      }
      let message = this.messages.find(x => x.pk === messagePk);
      if (!this.userCanEdit(message)) {
        return false;
      }
      let messageInput = document.querySelector('#message-input');
      if (this.messageBeingEdited != message.pk) {
        this.messageBeingEdited = message.pk;
        this.elFlicker(messageInput);
        this.messageUpdateText = message.content;
        this.$nextTick(() => {
          this.$refs.messageInputEdit.focus();
        })
      } else {
        this.messageBeingEdited = undefined;
        this.messageUpdateText = '';
      }
    },
    reverseUrl(view_name, params={}) {
      let args = '';
      if (Object.keys(params).length === 1) {
        args = '?' + Object.keys(params)[0] + '=' + Object.values(params)[0];
      }
      else if (Object.keys(params) && Object.keys(params).length > 1) {
        args += '?';
        for (let i = 0; i < Object.keys(params).length; i++) {
          args += Object.keys(params)[i] + '=' + Object.values(params)[i];
          if (i !== Object.keys(params).length - 1) {
            args += '&';
          }
        }
      }
      let lookupUrl = `/chat/api/urls/reverse/${view_name}/${args}`;
      var reversedUrl;
      let result = fetch(lookupUrl)
        .then(response => {
          if (!response.ok) {
              throw new Error("HTTP error, status = " + response.status);
            }
          return response.json();
        })
      return result;
    },
    handleResponse(response, responseType='json') {
      if (!response.ok) {
        this.displayStatusMessage("HTTP error, status = " + response.status);
        throw new Error("HTTP error, status = " + response.status);
        }
      if (responseType === 'none') {
        return undefined;
      }
      if (responseType === 'json') {
        return response.json();
      }
    },
    async conversationGetUsers() {
      let message = "Users in this conversation: \n\n";

      const urlParams = {
        'conversation_pk': this.conversationPk
      }
      const fetchUrl = await this.reverseUrl('api:conversation_user_list', urlParams);

      fetch(fetchUrl.url)
        .then(response => {return this.handleResponse(response);})
        .then(data => {
          for (let i in data) {
            message += `${Number(i) + 1}. ${data[i].username}\n`
          }
          window.alert(message);
        })
        .catch(error => console.log('conversationGetUsers(): Error: ' + error))

    },
    async messageGet(messagePk) {
      const urlParams = {
        'message_pk': messagePk
      }
      const fetchUrl = await this.reverseUrl('api:message_detail', urlParams);
      return fetch(fetchUrl.url)
      .then(response => {return this.handleResponse(response);})
    },
    async messagesGet() {
      if (this.allMessagesFetched) {
        return false;
      }
      const urlParams = {
        'conversation_pk': this.conversationPk,
        'message_count': this.messageDisplayCount
      }
      const fetchUrl = await this.reverseUrl('api:message_list_count', urlParams);
      this.topMessagePk = this.messages.slice(-1)[0].pk;
      fetch(fetchUrl.url)
      .then(response => {return this.handleResponse(response);})
      .then(data => {
        this.messages = data;
        if (data[0].all_messages_shown) {
          this.allMessagesFetched = true
        }
        // scroll down if user is at the bottom of the page
        this.$nextTick(() => {
          if (this.isScrolledToBottom()) {
            if (this.messages.length !== this.messageDisplayCount) {
              this.scrollToBottom();
            }
          }
          else {
            // scroll to top of highest previous message
            document.querySelector('#message' + this.topMessagePk).scrollIntoView();
          }
        })
        this.messageDisplayCount = this.messages.length;
      })
      .catch(error => console.log('Error: ' + error))
      this.messagesNewestDay = new Date(0);
    },
    messagesGetMore: function() {
      this.messageDisplayCount += 10;
      this.messagesGet();
    },
    async messageCreate() {

      if (!this.messageInputText) {
        return false;
      }

      const urlParams = {
        'conversation_pk': this.conversationPk
      }
      const fetchUrl = await this.reverseUrl('api:message_create', urlParams);

      const postData = {
        "content": this.messageInputText
      }

      fetch(fetchUrl.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        body: JSON.stringify(postData)
      })
      .then(response => {return this.handleResponse(response);})
      .then(data => {
        this.messages.splice(0, 0, data);
        this.messageInputText = '';
        this.messageDisplayCount = this.messages.length;
      })
      .then(() => this.scrollToBottom())
      .catch(error => console.log('messageCreate(): Error: ' + error))
    },
    async messageUpdate(messagePk) {

      if (!this.messageUpdateText) {
        this.messageUpdatePanelSelect(0);
        let statusMessage = "The updated message content was empty, so no changes have been made.<br><br>"
        statusMessage += "Please delete the message if you want to remove it."
        this.displayStatusMessage(statusMessage, timeout=5)
        return false;
      }
      else if (this.messageGetByPk(messagePk).content === this.messageUpdateText) {
        this.messageUpdatePanelSelect(0);
        let statusMessage = "The new message is the same as the old message.<br><br>";
        statusMessage += "The message has not been updated.";
        this.displayStatusMessage(statusMessage)
        return false;
      }

      if (this.messages.find(x => x.pk === messagePk).sender !== this.userPk) {
        let warningMessage = "This message belongs to another user and will be edited using admin privileges. "
        warningMessage += "Are you sure you want to edit this message?"
        if (!confirm(warningMessage)) {
          this.messageUpdatePanelSelect(0);
          return false;
        }
      }

      const urlParams = {'message_pk': messagePk}
      const fetchUrl = await this.reverseUrl('api:message_detail', urlParams);

      const postData = {
        "id": messagePk,
        "content": this.messageUpdateText
      }

      fetch(fetchUrl.url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        body: JSON.stringify(postData)
      })
      .then(response => {
        if (response.status === 404) {
          let statusMessage = "This message could not be found.<br><br>";
          statusMessage += "It may already have been deleted.";
          this.displayStatusMessage(statusMessage, 5000); 
          this.messageRemoveFromList(messagePk);
        }
        else {return this.handleResponse(response);}
      })
      .then(data => {
        this.displayStatusMessage('Message updated successfully.');
        // this.messages[this.messageGetIndexFromPk(messagePk)].content = this.messageUpdateText;
        Object.assign(this.messageGetByPk(messagePk), data);
        this.elFlicker(eval('this.$refs.message' + messagePk + '[0]'), '#393', 20, 300);
      })
      .catch(error => {
        console.log('Error: ' + error)
      })
      this.messageUpdatePanelSelect(0);
    },
    messageDeleteConfirm(messagePk) {
      if (confirm('Are you sure you want to delete this message? (ID: ' + messagePk + ')')) {
        this.messageDelete(messagePk);
      }
    },
    async messageDelete(messagePk) {
      const urlParams = {'message_pk': messagePk}
      const fetchUrl = await this.reverseUrl('api:message_detail', urlParams);
      fetch(fetchUrl.url, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
        }
      })
      .then(response => {
        if (!response.ok) {
          if (response.status === 404) {
            let statusMessage = "This message could not be found.<br><br>";
            statusMessage += "It may already have been deleted.";
            this.displayStatusMessage(statusMessage, 5000); 
            this.messageRemoveFromList(messagePk);
          }
          else {return this.handleResponse(response, 'none');}
        }
      })
      .then(() => {
        this.displayStatusMessage("Message deleted.");
        this.messageRemoveFromList(messagePk);
      })
    },
  }
})

// toggle the options menu with Esc
// document.addEventListener('keyup', function keyPress (e) {
//  if (e.key === 'Escape') {
//    app.optionsMenuShow = !app.optionsMenuShow;
//  }
//})
