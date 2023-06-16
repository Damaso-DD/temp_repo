const axios = require('axios');
const { expect } = require('chai');
// const shallowMount = require('@vue/test-utils');
// import SuggestionView from '../../src/views/SuggestionView.vue';



describe('GET /', () => {
    it('should respond with 200', async () => {
      const result = await axios.get('http://food', {});
      expect(result.status).to.eql(200);
    });
});

describe('GET /suggestions', () => {
    it('should respond with 200', async () => {
      // await axios.post('http://api/food', {'food': 'Rice'});
      const result = await axios.get('http://food/suggestions', {});
      expect(result.status).to.eql(200);
      // const wrapper = shallowMount(SuggestionView);
      // expect(wrapper.text()).to.include('Rice');

    });
});

describe('Fill food form', () => {
    it('should respond with 200', async () => {
      const result = await axios.post('http://api/food', {'food': 'Rice'});
      expect(result.status).to.eql(200);
    });
});
