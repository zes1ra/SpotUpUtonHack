<template>
  <div id="app">
    <div class="main">
      <div id="upload">
        <div>
          <h1>SpotUp</h1>
          <h4>post your personal data</h4>

          <form v-if="this.$root.$data.loading === false" class="margin-sm" @submit.stop.prevent="handleSubmit">
            <div class="border-style">
              <b-form-file plain @change="captureFile"/>
            </div>
            <b-form-textarea
              v-model="caption"
              placeholder="description"
              :rows="3"
              :max-rows="6"
              class="margin-xs"
            />
            <b-button class="margin-xs" variant="secondary" @click="handleOk">
              Upload
            </b-button>
          </form>
        </div>
        <div v-if="this.$root.$data.loading === true">
          <div class="spinner">
            <div class="rect1"></div>
            <div class="rect2"></div>
            <div class="rect3"></div>
            <div class="rect4"></div>
            <div class="rect5"></div>
          </div>
        </div>
      </div>

      <ul class="home-list">
        <li v-for="item in this.$root.$data.currentPosts" :key="item.key" :item="item">
          <b-card border-variant="secondary" :img-src="item.src">
            <p class="home-card-text">
              {{ item.caption }}
            </p>
          </b-card>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import ipfs from './contracts/ipfs';

export default {
  name: 'App',
  // data variables
  data() {
    return {
      buffer: '',
      caption: '',
    };
  },
  methods: {
    /* used to catch chosen image &
     * convert it to ArrayBuffer.
     */
    captureFile(file) {
      const reader = new FileReader();
      if (typeof file !== 'undefined') {
        reader.readAsArrayBuffer(file.target.files[0]);
        reader.onloadend = async () => {
          this.buffer = await this.convertToBuffer(reader.result);
        };
      } else this.buffer = '';
    },
    /**
     * converts ArrayBuffer to
     * Buffer for IPFS upload.
     */
    async convertToBuffer(reader) {
      return Buffer.from(reader);
    },
    /**
     * submits buffered image & text to IPFS
     * and retrieves the hashes, then store
     * it in the Contract via sendHash().
     */
    async onSubmit() {
      console.log('Uploading on IPFS');
      this.$root.loading = true;

      try {

        const hashedImg = await ipfs.add(this.buffer);
        const imgHash = hashedImg[0].hash;
        const bufferDesc = await this.convertToBuffer(this.caption);
        const hashedText = await ipfs.add(bufferDesc);
        const textHash = hashedText[0].hash;

        const transactionHash = await new Promise((acc, rej) => {
          this.$root.contract.methods
          .sendHash(imgHash, textHash)
          .send({ from: this.$root.currentAccount },
            (error, transactionHash) => {
              if (error) {
                rej(error)
              }
              else {
                acc(transactionHash)
              }
            });
        });

        if (typeof transactionHash !== 'undefined') {
          console.log('Storing on Ethereum');
          this.$root.contract.once('NewPost',
            { from: this.$root.currentAccount },
            () => {
              this.$root.getPosts();
              console.log('Operation Finished!');
            });
        } else {this.$root.loading = false;}

        } catch (e) {
          console.error(e);
          this.$root.loading = false;
      }
    },
    /**
     * validates if image & captions
     * are filled before submission.
     */
    handleOk() {
      if (!this.buffer || !this.caption) {
        alert('Please fill in the information.');
      } else {
        this.onSubmit();
      }
    },

  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  justify-content: center;
  color: #2c3e50;
  margin-top: 3%;
}

.main {
  display: flex;
  flex-direction: column;
}

.home-load {
  width: 50px;
  height: 50px;
}

.card img {
  object-fit: cover;
  height: 500px;
  width: 500px;
}

.card {
  text-align: left;
  width: 500px;
  margin-bottom: 20px;
}


.home-list{
  padding: 0;
  list-style: none;
}

.home-card-text {
  text-align: justify;
  margin-top: 10px;
}

#upload {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-bottom: 5%;
  width: 500px;
}

.spinner {
  margin: 100px auto;
  width: 50px;
  height: 40px;
  text-align: center;
  font-size: 10px;
}

.spinner > div {
  background-color: #333;
  height: 100%;
  width: 6px;
  display: inline-block;

  -webkit-animation: sk-stretchdelay 1.2s infinite ease-in-out;
  animation: sk-stretchdelay 1.2s infinite ease-in-out;
}

.spinner .rect2 {
  -webkit-animation-delay: -1.1s;
  animation-delay: -1.1s;
}

.spinner .rect3 {
  -webkit-animation-delay: -1.0s;
  animation-delay: -1.0s;
}

.spinner .rect4 {
  -webkit-animation-delay: -0.9s;
  animation-delay: -0.9s;
}

.spinner .rect5 {
  -webkit-animation-delay: -0.8s;
  animation-delay: -0.8s;
}

@-webkit-keyframes sk-stretchdelay {
  0%, 40%, 100% { -webkit-transform: scaleY(0.4) }
  20% { -webkit-transform: scaleY(1.0) }
}

@keyframes sk-stretchdelay {
  0%, 40%, 100% {
    transform: scaleY(0.4);
    -webkit-transform: scaleY(0.4);
  }  20% {
       transform: scaleY(1.0);
       -webkit-transform: scaleY(1.0);
     }
}

.margin-xs {
  margin-top: 3%;
}

.margin-sm {
  margin-top: 7%;
}

.border-style {
  border: 1px solid #ced4da;
}

</style>
