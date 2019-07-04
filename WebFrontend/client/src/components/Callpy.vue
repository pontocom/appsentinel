<template>
  <div>
    <p>RESPOSTA DO Callpy</p>
    <p>{{result}}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Callpy',
  data() {
    return {
      result: 'niente',
    };
  },
  methods: {
    getResult() {
      const self = this;
      const path = 'http://127.0.0.1:5000/androbugs';
      const args = {
        params: {
          type: '-f',
          apk: 'filename.apk',
        },
      };
      self.result = 'Androbugs';
      axios.get(path, args)
        .then((res) => {
          self.result = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getResult();
  },
};
</script>
