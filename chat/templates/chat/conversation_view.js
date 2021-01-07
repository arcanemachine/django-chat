"use strict";

let app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    userUsername: '{{ user.username }}',
    userPk: {{ user.pk }},
    userIsStaff: '{{ user.is_staff }}' === 'True',
    messages: '',
    messageInputText: '',
    messageUpdatePanelValue: undefined,
    messageUpdateStatus: '',
    messageUpdatedContent: '',
    menuShow: true
  },
  mounted() {
    this.getMessages();
    this.$nextTick(() => {
      this.scrollToBottom();
    })
    setInterval(() => {this.getMessages();}, 5000);
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
      let result = 0;
      for (let i = 0; i < username.length; i++) {
        result += username.codePointAt(i);
      }
      result = result % 14;
      if (result % 14 < 9) {
        result += 5;
      }
      return '#' + result.toString(16).repeat(6);
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
        console.log('is on bottom');
        return true;
      } else {
        console.log('is not on bottom');
        return false;
      }
    },
    scrollToBottom() {
      this.$refs.chatList.scrollTo(0, this.$refs.chatList.scrollHeight);
    },
    getMessages: function () {

      // REPLACE WITH DRF URL
      fetch('/chat/api/conversations/{{ conversation.pk }}/messages/')
        .then(response => {
          if (!response.ok) {
              throw new Error("HTTP error, status = " + response.status);
            }
          return response.json();
        })
        .then(data => {
          this.messages = data;
          if (this.scrolledToBottomOfElement(this.$refs.chatList)) {
            this.$nextTick(() => {
              this.scrollToBottom();
            });
          }
        })
        .catch(error => console.log('Error: ' + error.message))
      
    },
    getUserList() {
      window.alert('hello!');
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

document.addEventListener('keyup', function keyPress (e) {
  if (e.key === 'Escape') {
    app.menuShow = !app.menuShow;
  }
})
