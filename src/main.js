import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'babel-polyfill';
import App from './App.vue';
import web3 from './contracts/web3';
import contract from './contracts/contractInstance';

Vue.use(BootstrapVue);

// Vue instance
new Vue({
  el: '#app',
  data: {
    currentPosts: [],
    currentAccount: '',
    loading: true,
    contract,
  },

  async created() {
    await this.updateApp();
    new Promise((accept, reject) => {
      window.ethereum.on('accountsChanged', () => {
         this.updateApp().then(accept).catch(reject);
      })
    });
  },
  transformToRequire: {
    img: 'src',
    image: 'xlink:href',
  },
  methods: {
    async updateApp() {
      await this.updateAccount();
      await this.getPosts();
    },

    async updateAccount() {
      const accounts = await web3.eth.getAccounts();
      const account = accounts[0];
      this.currentAccount = account;
    },

    async getPosts() {
      this.loading = true;
      const posts = [];
      const counter = await contract.methods.getCounter().call({
        from: this.currentAccount,
      });

      if (counter !== null) {
        const hashes = [];
        const captions = [];
        for (let i = counter; i >= 1; i -= 1) {
          hashes.push(contract.methods.getHash(i).call({
            from: this.currentAccount,
          }));
        }

        const postHashes = await Promise.all(hashes);

        for (let i = 0; i < postHashes.length; i += 1) {
          captions.push(fetch(`https://gateway.ipfs.io/ipfs/${postHashes[i].text}`)
            .then(res => res.text()));
        }

        const postCaptions = await Promise.all(captions);


        for (let i = 0; i < postHashes.length; i += 1) {
          if (postHashes[i].owner === this.currentAccount) {
            posts.push({
              id: i,
              key: `key${i}`,
              caption: postCaptions[i],
              src: `https://gateway.ipfs.io/ipfs/${postHashes[i].img}`,
            });
          }
        }

        this.currentPosts = posts;
        this.loading = false;
      }
    },
  },
  render: h => h(App),
});
