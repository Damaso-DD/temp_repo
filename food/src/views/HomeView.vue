<script setup lang="ts">
import {  ref } from "vue";
import axios from 'axios';

var meal = ref('')
var message = ref('')

function submitForm(event: Event) {
  event.preventDefault()
  if (!meal.value) {
    sendMessage('Please fill the form before submitting.')
    return 
  }
  console.log(meal.value)
  var data = new FormData();
  data.append('food', meal.value)
  axios.post('http://api.suggestions.app.garden/food', {
    'food': meal.value
  }).then(function (response) {
      console.log(response)
      sendMessage('Thank you for your suggestion!')
  }).catch(function (error: Error){
    console.log(error);
    sendMessage('An error occurred. Please try again')
  });
}


function sendMessage(msg:string) {
  message.value = msg
  setTimeout(function(){
    message.value = ''
  }, 2000)
  meal.value = ''
}
</script>

<template>
  <main class="ui raised segment">
    <div class="ui message" v-show="message">{{ message }}</div>
    <form class="ui form">
      <div class="ui form field">
        <label for="name">Suggest a meal</label>
        <input v-model="meal" type="text" name="food"/>
      </div>
      <button v-on:click="submitForm" class="ui button primary big" type="submit">Enter</button>
    </form>
  </main>
</template>

<style scoped>
 .ui.form.field >  label {
  font-size: 15px;
  padding-bottom: 10px;
 }
</style>
