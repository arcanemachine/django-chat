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
    userUsername: '{{ user.username }}',
    userPk: {{ user.pk }},
    userIsStaff: '{{ user.is_staff }}' === 'True',
    messages: JSON.parse(conversationMessages),
    allMessagesShown: false,
    messageDisplayCount: 10,
    messageInputText: '',
    messageUpdatePanelValue: undefined,
    messageUpdateStatus: '',
    messageUpdatedContent: '',
    menuShow: false,

    isMounted: false

  },
  mounted() {
    
    // scroll to bottom of chatList
    this.$nextTick(() => {
      this.scrollToBottom();
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
        'background-color': this.getBackgroundColor(message.fields.sender_username),
      }
    },
    getBackgroundColor(username) {
      let maxValue = 255 - 16;
      let minValue = 128 + 32;
      let result = '';
      for (let i = 0; i < 3; i++) {
        let seed = new Math.seedrandom(username.substr(i, i+1))();
        let thisResult = maxValue - Math.floor(seed * maxValue);
        result += thisResult.toString(16);
      }
      return '#' + result;
    },
    userIsSender: function (message) {
      if (message.fields.sender === this.userPk) {
        return true;
      } else return false;
    },
    userCanEdit: function (message) {
      if (this.userIsStaff) {
        return true;
      }
      else if (this.userPk === message.fields.sender) {
        return true;
      }
      else {
        return false;
      }
    },
    messageUpdatePanelSelect: function (messagePk) {
      if (this.messageUpdatePanelValue != messagePk) {
        this.messageUpdatePanelValue = messagePk;
        this.messageUpdatedContent = this.messages[messagePk-1].fields.content;
      } else {
        this.messageUpdatePanelValue = undefined;
        this.messageUpdatedContent = '';
      }
    },
    scrolledToBottomOfElement(el) {
      let elementTotalHeight = el.scrollHeight;
      let elementVisibleHeight = el.clientHeight;
      let elementScrollHeight = el.scrollHeight - el.clientHeight;
      if (el.scrollTop === elementScrollHeight) {
        return true;
      } else {
        return false;
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.chatList.scrollTo(0, this.$refs.chatList.scrollHeight);
      })
    },
    reverseUrl(view_name, params={}) {
      let args = '';
      if (Object.keys(params).length === 1) {
        args = '?' + Object.keys(params)[0] + '=' + Object.values(params)[0];
      }
      else if (Object.keys(params).length > 1) {
        args += '?';
        for (let i = 0; i < Object.keys(params).length; i++) {
          args += Object.keys(params)[i] + '=' + Object.values(params)[i];
          if (i !== Object.keys(params).length - 1) {
            args += '&';
          }
        }
      }
      let result = `/chat/api/urls/reverse/${view_name}/${args}`;
      console.log(result);
      return result
    },
    getMessages: function () {

      if (this.allMessagesShown) {
        return;
      }

      // REPLACE WITH DRF URL
      let fetchUrl = undefined;
      fetch(`/chat/api/conversations/{{ conversation.pk }}/messages/${this.messageDisplayCount}`)
        .then(response => {
          if (!response.ok) {
              throw new Error("HTTP error, status = " + response.status);
            }
          return response.json();
        })
        .then(data => {
          this.messages = data.messages;
          this.messageDisplayCount = data.messages.length;
          if (data.allMessagesShown) {
            this.allMessagesShown = true
          }
          
          // scroll down if user is at the bottom of the page
          this.$nextTick(() => {
            if (this.scrolledToBottomOfElement(this.$refs.chatList)) {
                this.scrollToBottom();
            }
          })

        })
        .catch(error => console.log('Error: ' + error.message))
      
    },
    getMoreMessages: function() {
      this.messageDisplayCount += 10;
      this.getMessages();
    },
    getUserList() {
      let message = "Users in this conversation: \n\n";

      fetch('/chat/api/conversations/{{ conversation.pk }}/users/')
        .then(response => {
          if (!response.ok) {
              throw new Error("getUserList(): HTTP error, status = " + response.status);
            }
          return response.json();
        })
        .then(data => {
          for (let i in data) {
            message += `${Number(i) + 1}. ${data[i].fields.username}\n`
          }
          window.alert(message);
        })
        .catch(error => console.log('getUserList(): Error: ' + error.message))

    },
    messageSend() {
      fetch('/chat/api/conversations/1/messages/create/')
        .then(response => {
          if (!response.ok) {
            if (response.status === 403) {
              this.displayStatusMessage('You do not have permission to modify this message.');
            }
            throw new Error("HTTP error, status = " + response.status);
            }
          return response.json();
        })
         .then(data => {console.log(data)})
      this.getMessages();
    },
    messageUpdate: function (messagePk) {

      const csrfToken = Cookies.get('csrftoken');

      const postData = {
        "id": this.messagePk,
        "content": this.messageUpdatedContent
      }

      fetch(`/api/v1/messages/${messagePk}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
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
        console.log('Error: ' + error.message)
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
