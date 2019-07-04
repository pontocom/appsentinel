<template>
  <div class="home">
    <img alt="logo" src="../assets/templogo.png">
    <br/><br/>
    <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
    <button v-on:click="submitFile()">GO!</button>
    <br/><br/>
    <div v-if="loading" class="lds-ripple"><div></div><div></div></div>
    <p> {{msg}} </p>
    <p> {{otherMsg}} </p>

    <table v-if="done" id="simpleTable">
      <thead>
        <tr>
          <th>Level</th>
          <th>CVE</th>
          <th>Analysis</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" v-bind:key="row.id">
          <td :style="{ 'color': row.level == 'Critical' ? 'red' :
                                 row.level == 'Warning' ? 'orange' :
                                 row.level == 'Info' ? 'green' : 'black'
           }" >{{row.level}}</td>
          <td style="min-width: 200px">{{row.cve}}</td>
          <td>{{row.analysis}}</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Start',

  data() {
    return {
      file: '',
      msg: '',
      otherMsg: '',
      loading: false,
      done: false,
      rows: [],
    };
  },

  methods: {
    submitFile() {
      const self = this;
      const path = 'http://127.0.0.1:5000/upload-file';
      const header = {
        'Content-Type': 'multipart/form-data',
      };
      const formData = new FormData();
      self.loading = true;
      formData.append('file', self.file);
      self.msg = 'Uploading';
      axios.post(path, formData, header)
        .then((res) => {
          self.msg = `Done uploading: ${res.data}`;
          self.rows = [];
          setTimeout(() => {
            self.getResults(res.data);
          }, 1000);
        })
        .catch((error) => {
          self.msg = `Uploading Error: ${error}`;
          self.loading = false;
        });
    },
    handleFileUpload() {
      [this.file] = this.$refs.file.files;
    },
    async getResults(filename) {
      const self = this;
      await self.getResultFromAndrobugs(filename);
      self.deleteFile(filename);
      self.otherMsg = 'end';
    },
    async getResultFromAndrobugs(filename) {
      const self = this;
      const path = 'http://127.0.0.1:5000/androbugs';
      const args = {
        params: {
          type: '-f',
          apk: filename,
        },
      };
      self.msg = `Analyzing with ANDROBUGS: ${filename}`;
      const androbugsCall = axios.get(path, args)
        .then((res) => {
          self.msg = 'Importing ANDROBUGS results';
          const androbugsResult = res.data.details;
          Object.keys(androbugsResult).forEach((key) => {
            self.rows.push({
              id: self.rows.length,
              level: androbugsResult[key].level,
              cve: androbugsResult[key].cve_number,
              analysis: androbugsResult[key].title,
            });
          });
          self.msg = '';
          self.loading = false;
          self.done = true;
        })
        .catch((error) => {
          self.msg = `Androbugs Error: ${error}`;
          self.loading = false;
        });
      await new Promise((resolve) => {
        resolve(androbugsCall);
      });
    },
    deleteFile(filename) {
      const self = this;
      const path = 'http://127.0.0.1:5000/delete-apk';
      const args = {
        params: {
          apk: filename,
        },
      };
      axios.get(path, args)
        .then((res) => {
          self.msg = res.data;
          self.loading = false;
          self.done = true;
        })
        .catch((error) => {
          self.msg = `Temporary Error: ${error}`;
          self.loading = false;
        });
    },
  },
};
</script>

<style>
.lds-ripple {
  display: inline-block;
  position: relative;
  width: 64px;
  height: 64px;
}
.lds-ripple div {
  position: absolute;
  border: 4px solid rgb(14, 87, 221);
  opacity: 1;
  border-radius: 50%;
  animation: lds-ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}
.lds-ripple div:nth-child(2) {
  animation-delay: -0.5s;
}
@keyframes lds-ripple {
  0% {
    top: 28px;
    left: 28px;
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    top: -1px;
    left: -1px;
    width: 58px;
    height: 58px;
    opacity: 0;
  }
}
table {
  font-family: 'Open Sans', sans-serif;
  width: 750px;
  border-collapse: collapse;
  border: 3px solid #44475C;
  /* margin: 10px 10px 0 10px; */
  margin: 0px auto;
}

table th {
  text-transform: uppercase;
  text-align: left;
  background: #44475C;
  color: #FFF;
  padding: 8px;
  min-width: 50px;
}

table td {
  text-align: left;
  padding: 8px;
  border-right: 2px solid #7D82A8;
  min-width: 100px;
}
table td:last-child {
  border-right: none;
}
table tbody tr:nth-child(2n) td {
  background: #D4D8F9;
}
</style>
