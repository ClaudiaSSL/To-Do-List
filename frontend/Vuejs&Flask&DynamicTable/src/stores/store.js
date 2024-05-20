import { defineStore } from 'pinia'
import axios from 'axios';

export const tasksStore = defineStore("tasks-store", {
  state: () => ({
        tasks: [],
        message: '',
        showMessage: false,
    }),
  actions: {
    addTask(payload) {
        const path = 'http://localhost:5001/tasks';
        axios.post(path, payload)
          .then(() => {
            this.tasks = this.getTasks();
            this.message = 'Task added!';
            this.showMessage = true;
          })
          .catch((error) => {
            console.log(error);
            this.getTasks();
          });
      },
      
      updateTask(payload, taskID) {
        const path = `http://localhost:5001/tasks/${taskID}`;
        axios.put(path, payload)
            .then(() => {
              this.getTasks();
              this.message = 'Task updated!';
              this.showMessage = true;
            })
            .catch((error) => {
              console.error(error);
              this.getTasks();
            });
        },

        removeTask(taskID) {
          const path = `http://localhost:5001/tasks/${taskID}`;
          axios.delete(path)
              .then(() => {
                this.getTasks();
                this.message = 'Task removed!';
                this.showMessage = true;
              })
              .catch((error) => {
                console.error(error);
                this.getTasks();
              });
      },

      getTasks(){
          const path = 'http://localhost:5001/tasks';
          axios.get(path)
            .then((res) => {
              this.tasks=res.data.tasks
            })
            .catch((error) => {
              console.error(error);
            })     
      },

      getAutocomplete(table, column, value){
        const payload = {
          table : table,
          column : column,
          value : value
        }
        const path = 'http://localhost:5001/autocomplete';
          return axios.post(path, payload)
            .then((res) => {
              return res.data.autocomplete
            })
            .catch((error) => {
              console.error(error);
            }) 
      }
  },

});


