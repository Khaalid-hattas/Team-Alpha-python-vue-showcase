import axios from 'axios';

const API = axios.create ({
  baseURL: 'http://localhost:5000/api'
});

export default {
  getItems() {return API.get('/items');},
  triggerScrape() {return API.post('/scrape');},
  search(query) {return API.get(`/search?q=${query}`);},
  getStats() {return API.get('/statistics');}
}