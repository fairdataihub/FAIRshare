import { createStore } from "vuex";

export default createStore({
  state: {
    user: {
      name: "Test User",
      email: "testuser@fairdataihub.org",
      username: "tufdih",
    },
    posts: ["post 1", "post 2", "post 3", "post 4"],
    errors: [],
  },
  getters: {
    postsCount(state) {
      return state.posts.length;
    },
    postsCountMessage: (_state, getters) =>
      `${getters.postsCount} posts available`,
  },
  mutations: {
    INSERT_POST(state, post) {
      state.posts.push(post);
    },
    INSERT_ERROR(state, error) {
      state.errors.push(error);
    },
  },
  actions: {
    async insertPost({ commit }, payload) {
      //make some kind of ajax request
      try {
        // await doAjaxRequest(payload)
        // can commit multiple mutations in an action
        commit("INSERT_POST", payload);
      } catch (error) {
        commit("INSERT_ERROR", error);
      }
    },
  },
});
