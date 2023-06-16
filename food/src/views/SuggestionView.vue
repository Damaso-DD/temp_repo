
<script setup>
import axios from 'axios';
import {ref} from 'vue';

var suggestions = ref([]);

var showSugg = ref(false)

fetchSuggestions()

function fetchSuggestions () {
  axios.get('http://api.suggestions.app.garden/food')
  .then(function(response) {
    console.log(response)
    suggestions.value = response.data.suggestions
    console.log(suggestions.value)
    showSugg.value = true
  }).catch(function(error) {
    console.error(error)
  })

}


</script>


<template>
  <div class="suggestions">
    <div class="ui wide raised stacked segment">
      <h4>All Suggestions to the Menu</h4>
      <!-- <div class="ui message" v-hide="showSugg">Drat! No suggestions yet.</div> -->
      <ul>
        <li v-for="(item, index) in suggestions" v-bind:key="index">
          {{ item.name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .suggestions {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
  
  .suggestions .ui.segment {
    min-height: 50vh;
    min-width: 50px;
  }
}
</style>
