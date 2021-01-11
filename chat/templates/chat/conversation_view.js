"use strict";

  // indented stuff is django-related
  </script>
  {{ conversation_messages|json_script:'conversation-messages' }}
  <script>
  let conversationMessages = document.querySelector('#conversation-messages').textContent;

  // hide non-js form
  document.querySelector('#non-js-form').style['display'] = 'none';

let app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    conversationPk: {{ conversation.pk }},
    userUsername: '{{ user.username }}',
    userPk: {{ user.pk }},
    userIsStaff: '{{ user.is_staff }}' === 'True', // do a boolean check for python's True/False boolean style
    userBackgroundColors: {},
    messages: JSON.parse(conversationMessages),
    allMessagesShown: false,
    messageDisplayCount: 10,
    messageInputText: '',
    messageBeingEdited: undefined,
    messageUpdateText: '',
    menuShow: false,

    statusMessage: '',
    statusMessageTimeout: undefined,

  },
  computed: {
    messagesReversed() {
      return this.messages.slice().reverse();
    }
  },
  created() {
    this.getMessages = _.debounce(this.getMessages, 400, {
      leading: true,
      trailing: false
    })
  },
  mounted() {
    
    // scroll to bottom of chatList
    this.$nextTick(() => {
      this.scrollToBottom(smooth=false);
    })

    // when scrolled to top of chatList, load 10 more messages
    var chatList = document.querySelector('.chat-list');
    chatList.addEventListener('scroll', (e) => {
      if (chatList.scrollTop === 0) {
        this.getMoreMessages();
        this.$nextTick(() => {
          chatList.scrollTop = 1;
        })
      }
    })

    // poll for new messages every 5 seconds
    setInterval(() => {this.getMessages();}, 5000);
    
  },
  methods: {
    messageContentClass: function (message) {
      return {
        'bold': this.userCanEdit(message),
        'cursor-url': this.userCanEdit(message),
        'item-current-user': this.userIsSender(message),
        'item-other-user': !this.userIsSender(message),
      }
    },
    messageContentStyle: function (message) {
      return {
        'background-color': this.getBackgroundColor(message.sender_username),
      }
    },
    elFlicker(el, flickerColor='#99f', startAfter=20, stopAfter=360) {
      let originalColor = el.style.backgroundColor;
      setTimeout(() => {
        el.style.backgroundColor = flickerColor;
      }, startAfter)
      setTimeout(() => {
        el.style.backgroundColor = originalColor;
      }, stopAfter)
    },
    menuToggle() {
      this.menuShow = !this.menuShow;
    },
    getBackgroundColor(username) {
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
    messageGetIndex(messagePk) {
      let pkList = [];
      for (let i = 0; i < this.messages.length; i++) {
        pkList.push(this.messages[i].pk)
      }
      let index = pkList.indexOf(messagePk)
      return index;
    },
    messageGetFromPk(messagePk) {
      return this.messages[this.messageGetIndex(messagePk)];
    },
    messageRemoveFromList(messagePk) {
      let index = this.messageGetIndex(messagePk);

      // shrink the deleted message along the y-axis
      let messageEl = eval('this.$refs.message' + messagePk)[0];
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
      message = this.messages.find(x => x.pk === messagePk);
      if (!this.userCanEdit(messagePk)) {
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
    async getConversationUsers() {
      let message = "Users in this conversation: \n\n";

      const urlParams = {
        'conversation_pk': this.conversationPk
      }
      const fetchUrl = await this.reverseUrl('api:conversation_user_list', urlParams);

      fetch(fetchUrl.url)
        .then(response => {
          if (!response.ok) {
              this.displayStatusMessage("getConversationUsers(): HTTP error, status = " + response.status);
                throw new Error("getConversationUsers(): HTTP error, status = " + response.status);
              }
            return response.json();
          })
          .then(data => {
            for (let i in data) {
              message += `${Number(i) + 1}. ${data[i].username}\n`
            }
            window.alert(message);
          })
          .catch(error => console.log('getConversationUsers(): Error: ' + error))

    },
    async getMessages() {
      if (this.allMessagesShown) {
        return;
      }
      const urlParams = {
        'conversation_pk': this.conversationPk,
        'message_count': this.messageDisplayCount
      }
      const fetchUrl = await this.reverseUrl('api:message_list_count', urlParams);
      this.topPageMessage = document.querySelector('#message' + this.messages.slice(-1)[0].pk);
      fetch(fetchUrl.url)
        .then(response => {
          if (!response.ok) {
              throw new Error("HTTP error, status = " + response.status);
            }
          return response.json();
        })
        .then(data => {
          this.messages = data;
          if (data[0].all_messages_shown) {
            this.allMessagesShown = true
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
              this.topPageMessage.scrollIntoView();
            }
          })
          this.messageDisplayCount = this.messages.length;
        })
        .catch(error => console.log('Error: ' + error))
    },
    getMoreMessages: function() {
      this.messageDisplayCount += 10;
      this.getMessages();
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
      .then(response => {
        if (!response.ok) {
          this.displayStatusMessage("HTTP error, status = " + response.status);
          throw new Error("HTTP error, status = " + response.status);
          }
        return response.json();
      })
      .then(data => {
        console.log(data)
        this.messages.splice(0, 0, data);
        this.messageInputText = '';
        this.messageDisplayCount = this.messages.length;
      })
      .then(() => this.scrollToBottom())
      .catch(error => console.log('messageCreate(): Error: ' + error))
    },
    async messageUpdate(messagePk) {

      if (!this.messageUpdateText) {
        this.messageBeingEdited = undefined;
        let statusMessage = "The updated message content was empty, so no changes have been made.<br><br>"
        statusMessage += "Please delete the message if you want to remove it."
        this.displayStatusMessage(statusMessage, timeout=5)
        return false;
      }
      else if (this.messageGetFromPk(messagePk).content === this.messageUpdateText) {
        let statusMessage = "The new message is the same as the old message.<br><br>";
        statusMessage += "The message has not been updated.";
        this.displayStatusMessage(statusMessage)
        return false;
      }

      if (this.messages.find(x => x.pk === messagePk).sender !== this.userPk) {
        let warningMessage = "This message belongs to another user and will be edited using admin privileges. "
        warningMessage += "Are you sure you want to edit this message?"
        if (!confirm(warningMessage)) {
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
        if (!response.ok) {
          this.displayStatusMessage("HTTP error, status = " + response.status);
          throw new Error("HTTP error, status = " + response.status);
          }
        return response.json();
      })
      .then(() => {
        this.displayStatusMessage('Message updated successfully.');
        this.elFlicker(eval('this.$refs.message' + messagePk + '[0]'), '#393', 20, 1020);
        this.messages[this.messageGetIndex(messagePk)].content = this.messageUpdateText;
      })
      .catch(error => {
        console.log('Error: ' + error)
      })
      this.messageBeingEdited = undefined;
    },
    handleResponse(response) {
      if (!response.ok) {
        this.displayStatusMessage("HTTP error, status = " + response.status);
        throw new Error("HTTP error, status = " + response.status);
        }
      return response.json();
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
          }
          else {
            this.displayStatusMessage("HTTP error, status = " + response.status);
            throw new Error("HTTP error, status = " + response.status);
          }
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
//    app.menuShow = !app.menuShow;
//  }
//})
