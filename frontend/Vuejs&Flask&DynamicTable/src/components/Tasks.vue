<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>My To Do List</h1>
        <alert :message="store_tasks.message" v-if="store_tasks.showMessage"></alert>
        <div style="height: 80px;"></div>
        <table id="table" class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Description</th>
              <th scope="col">For</th>
              <th scope="col">Done?</th>
              <th></th>
            </tr>
          </thead>
          <tbody autocomplete='off' id="tbody">
            <tr v-for="(task, index) in tasks" :key="index">
              <td id="line" v-if="desc_cell_editable == index">
                <autocomplete v-model="editTaskForm.task_description"  :subject="'description'" :placeholder="task.description" @click="changeTask(task, index)"
                              @focusout="onClickOutside(task)"/>
              </td>
              <td @click="onClickDescription(task, index)" v-else>
                {{ task.description }}
              </td>
              <td id="editTaskFor" v-if="for_cell_editable == index" >
                <autocomplete v-model="editTaskForm.task_for"  :subject="'about'"  :placeholder="task.about"
                            @click="changeTask(task, index)" @focusout="editTask(task)"/>
              </td>
              <td @click="onClickFor(task, index)" v-else>
                {{ task.about }}
              </td>
              <td>
                <tswitch v-model="task.done" @click="changeTask(task)" @focusout="editTask(task)"></tswitch >
              </td>
              <td>
                <div class="btn-group" role="group">
                       <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="store_tasks.removeTask(task.id)">
                        Delete
                    </button>
                </div>
              </td>
            </tr>
            <tr >
              <td>
                <autocomplete v-model="addTaskForm.task_description" :subject="'description'" :placeholder="'Describe the task. For example: Read book XPTO'"/>
              </td>
              <td>
                <autocomplete v-model="addTaskForm.task_for"  :subject="'about'" :placeholder="'Enter for what task is. For example: Home'"/>
              </td>
              <td>
                <tswitch v-model="addTaskForm.task_done" ></tswitch>
                
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button"
                      class="btn btn-success btn-sm"
                      @click="addField()" 
                      >
                      Add task
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>

import Alert from './Alert.vue';
import TSwitch from './ToggleSwitch.vue';
import { tasksStore } from "../stores/store";
import { mapActions , mapState} from 'pinia'
import autocomplete from './Autocomplete.vue';


export default {
  
  data() {
    return {
      store_tasks: tasksStore(),
      addTaskForm: {
          task_description: '',
          task_for: '',
          task_done: false,
        },
      editTaskForm: {
          task_id:'',
          task_description: '',
          task_for: '',
          task_done: false,
      },
      desc_cell_editable:-1,
      for_cell_editable:-1,
    };
  },

  components: {
    alert: Alert,
    tswitch: TSwitch,
    autocomplete: autocomplete,
  },

  computed:{
    ...mapState(tasksStore, ['tasks'])
  },
  
  methods: {
    ...mapActions(tasksStore, ['getTasks']),

    //function to allow the changes in the tasks to be saved when click outside the input field
    onClickOutside(task){
      this.editTask(task)
      let el = document.getElementById('input')
      el.style.border = 0
    },

    //function to do when click on description field to edit
    onClickDescription(task, index){
      //to be possible to edit only the selected input field
      this.desc_cell_editable=index 
      this.changeTask(task)
      this.editTask(task)
    },

     //function to do when click on for field to edit
    onClickFor(task, index){
      this.for_cell_editable=index
      this.changeTask(task)
      this.editTask(task)
    },

    //pass all task varibles to component variables to pass the new info into update function as payload
    changeTask(task){
      //give a little time to v-model perform
      setTimeout(()=>{
        this.editTaskForm.task_id =task.id
        this.editTaskForm.task_for = task.about
        this.editTaskForm.task_description = task.description
        this.editTaskForm.task_done=task.done
      },200)
      
    },

    //To add a new task when clich on Add task button
    addField(){ 
      //compose the payload info required on addTask function (store)
      const payload = { 
            description: this.addTaskForm.task_description,
            for: this.addTaskForm.task_for,
            done: this.addTaskForm.task_done, 
          };
          //execute addTask function (store) that will add this task
          this.store_tasks.addTask(payload) 
          //clean component variables 
          this.addTaskForm.task_description = ''  
          this.addTaskForm.task_for=''
          this.addTaskForm.task_done=false
    },

    editTask(task){
      
      if (this.editTaskForm.task_id != ''){
        const payload = {
          id : this.editTaskForm.task_id,
          description :this.editTaskForm.task_description,
          for : this.editTaskForm.task_for,
          done : this.editTaskForm.task_done
        };
        //execute updateTask function (store) that will update the task
        this.store_tasks.updateTask(payload, task.id)
        //run getTasks funstion (store) and get all the tasks to update the table 
        this.store_tasks.getTasks()
      }
    },
  },
  created() {
      //run getTasks funstion (store) when component is created and get all the tasks to populate the table
      this.store_tasks.getTasks()  
  },
};
</script>
<style scoped>
.switch {
  position: relative;
  display: inline-block;
  width: 51px;
  height: 32px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.btn{
  width:72px;
}

li{
  list-style-type: none;
}
</style>