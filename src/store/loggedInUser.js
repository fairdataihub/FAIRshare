import { defineStore } from "pinia";

export const useLoggedInUserStore = defineStore({
  // id is required so that Pinia can connect the store to the devtools
  id: "loggedInUser",
  state: () => ({
    name: "John Doe",
    email: "fake@email.com",
    username: "jd123",
    posts: ["post 1", "post 2", "post 3", "post 4"],
  }),
  getters: {},
  actions: {},
});
