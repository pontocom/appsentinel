import Vue from 'vue';
import Router from 'vue-router';
import Start from './components/Start.vue';
import Callpy from './components/Callpy.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'start',
      component: Start,
    },
    {
      path: '/callpy',
      name: 'Callpy',
      component: Callpy,
    },
  ],
});
