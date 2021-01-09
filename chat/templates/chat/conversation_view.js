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
    messageUpdatePanelValue: undefined,
    messageUpdateStatus: '',
    messageUpdatedContent: '',
    menuShow: false,

    isMounted: false,

  },
  computed: {
    messagesReversed() {
      return this.messages.slice().reverse();
    }
  },
  mounted() {
    
    // scroll to bottom of chatList
    this.$nextTick(() => {
      this.scrollToBottom(smooth=false);
    })

    // when scrolled to top of chatList, load 10 more messages
    setTimeout(() => {
      var chatList = document.querySelector('.chat-list');
      chatList.addEventListener('scroll', (e) => {
        if (chatList.scrollTop === 0) {
          this.getMoreMessages();
          this.$nextTick(() => {
            chatList.scrollTop = 1;
          })
        }
      })
    }, 500)

    // poll for new messages every 5 seconds
    // setInterval(() => {this.getMessages();}, 5000);
    
    this.isMounted = true;

  },
  methods: {
    toggleMenu() {
      this.menuShow = !this.menuShow;
    },
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
    messageUpdatePanelSelect: function (messagePk) {
      if (this.messageUpdatePanelValue != messagePk) {
        this.messageUpdatePanelValue = messagePk;
        this.messageUpdatedContent = this.messages.find(x => x.id === messagePk).content;
      } else {
        this.messageUpdatePanelValue = undefined;
        this.messageUpdatedContent = '';
      }
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
    async getMessages() {

      if (this.allMessagesShown) {
        return;
      }

      // REPLACE WITH DRF URL
      const urlParams = {
        'conversation_pk': this.conversationPk,
        'message_count': this.messageDisplayCount
      }
      // let fetchUrl = await this.reverseUrl('chat:get_conversation_messages', urlParams);
      const fetchUrl = await this.reverseUrl('api:message_list_count', urlParams);
      let topMessage = document.querySelector('#message' + this.messages.slice(-1)[0].pk);
      fetch(fetchUrl.url)
        .then(response => {
          if (!response.ok) {
              throw new Error("HTTP error, status = " + response.status);
            }
          return response.json();
        })
        .then(data => {
          this.messages = data;
          if (data.allMessagesShown) {
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
              topMessage.scrollTo(0, 0);
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
    async getUserList() {
      let message = "Users in this conversation: \n\n";

      const urlParams = {
        'conversation_pk': this.conversationPk,
      }
      const fetchUrl = await this.reverseUrl('api:conversation_user_list', urlParams);
      fetch(fetchUrl.url)
        .then(response => {
          if (!response.ok) {
              this.displayStatusMessage("getUserList(): HTTP error, status = " + response.status);
              throw new Error("getUserList(): HTTP error, status = " + response.status);
            }
          return response.json();
        })
        .then(data => {
          for (let i in data) {
            message += `${Number(i) + 1}. ${data[i].username}\n`
          }
          window.alert(message);
        })
        .catch(error => console.log('getUserList(): Error: ' + error))

    },
    async messageSend() {

      const csrftoken = Cookies.get('csrftoken');
      const urlParams = {
        'conversation_pk': this.conversationPk,
      }
      const postData = {
        "content": this.messageInputText
      }

      let fetchUrl = await this.reverseUrl('api:message_create', urlParams);
      fetch(fetchUrl.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
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
        if (data.allMessagesShown) {
          this.allMessagesShown = true
        }
      })
      .then(() => this.scrollToBottom())
      .catch(error => console.log('messageSend(): Error: ' + error))
    },
    messageUpdate: function (messagePk) {

      const csrftoken = Cookies.get('csrftoken');

      const postData = {
        "id": this.messagePk,
        "content": this.messageUpdatedContent
      }

      fetch(`/api/v1/messages/${messagePk}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(postData)
      })
      .then(response => {
        if (!response.ok) {
          if (response.status === 403) {
            this.displayStatusMessage('You do not have permission to modify this message.');
          }
          throw new Error("HTTP error, status = " + response.status);
          }
        return response.json();
      })
      .then(() => {
        this.displayStatusMessage('Message updated successfully.');
        this.getMessages();
      })
      .catch(error => {
        console.log('Error: ' + error)
      })
      this.messageUpdatePanelValue = undefined;
    },
    displayStatusMessage: function (message) {
      this.messageUpdateStatus = message;
      setTimeout(() => {
        this.messageUpdateStatus = '';
        this.messageUpdatePanelValue = undefined;
      }, 3000)
    }
  }
})

// toggle the options menu with Esc
document.addEventListener('keyup', function keyPress (e) {
  if (e.key === 'Escape') {
    app.menuShow = !app.menuShow;
  }
})
