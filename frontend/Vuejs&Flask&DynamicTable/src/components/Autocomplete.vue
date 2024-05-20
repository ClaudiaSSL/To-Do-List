<template>
    <div  class="autocomplete">
        <input
                autocomplete='off' id='input' class="form-control" type="text"  v-model="search"  @input="onChange" 
                @click="setInitialSearchValue" @keydown.down="onArrowDown" @keydown.up="onArrowUp" @keydown.enter.prevent="onEnter" 
                :placeholder='placeholder' @focusout="clickOutside"
        />
        <ul id="autocomplete-results" 
            v-show="isOpen" class="autocomplete-results">
            <li class="loading"
                v-if="isLoading">
                Loading results...
            </li>
            <li v-else
                v-for="(result, i) in results" id="input_li"
                :key="i" @click="setResult(result)" class="autocomplete-result"
                :class="{ 'is-active': i === arrowCounter }">
                {{ result }}
            </li>
        </ul>
    </div>
        
</template>

<script>
import { tasksStore } from "../stores/store";
import { mapActions, mapState } from 'pinia'


export default {
        name: "autocomplete",
        props: ['subject','placeholder','modelValue'],  
        emits: ['update:modelValue', 'update:isOpen'],
        computed: {
            ...mapState(tasksStore, ['tasks']),
        },
        watch: { 
            modelValue: function(new_val, old_val){
                this.search = new_val
            },
            search: function(new_val, old_val){
                this.$emit('update:modelValue', new_val) 
            },
            isOpen: function(new_val, old_val){
                this.$emit('update:isOpen', new_val) 
            }
        },
        data() {
            return {
                store_tasks: tasksStore(),
                isOpen: false,
                results: [],
                search: '',
                isLoading: false,
                arrowCounter: 0,
                items:[],
                perPage:100,
                pageNumber:1,
                
            } 
        },
        methods: {
            ...mapActions(tasksStore, ['getAutocomplete']),

            clickOutside(){
                setTimeout(()=>{
                    this.isOpen = false;
                },200)
                
            },
            setInitialSearchValue(){
                this.search = this.modelValue
            },

            onChange(event) {
                this.store_tasks.getAutocomplete('tasks',this.subject, this.search)
                    .then((options)=>{
                        if(options.length > 0){
                            this.results = options
                            this.isOpen = true;
                            this.filterResults();
                        }else{
                            console.log('no options')
                        }
                            
                    })
            },

            filterResults() {
                // first uncapitalize all the things
                this.items = this.results.filter((item) => {
                    return item.toLowerCase().indexOf(this.search.toLowerCase()) > -1;
                });
            },
            setResult(result) {
                this.search = result;
                this.isOpen = false;
                
            },
            onArrowDown(evt) {
                if (this.arrowCounter < this.results.length) {
                    this.arrowCounter = this.arrowCounter + 1;
                }
            },
            onArrowUp() {
                if (this.arrowCounter > 0) {
                    this.arrowCounter = this.arrowCounter - 1;
                }
                
            },
            onEnter() {
                this.search = this.results[this.arrowCounter];
                this.isOpen = false;
                this.arrowCounter = -1;
            },

            close(){
                this.isOpen = false;
            }
        },
}
</script>

<style scoped>
.autocomplete {
    position: relative;
}

.autocomplete-results {
    z-index: 1000;
    position: absolute;
    padding: 0;
    margin: 0;
    border: 1px solid rgb(186, 206, 228);
    border-radius: 4px;
    height: 120px;
    overflow: auto;
    width: 100%;
    background-color: white;
}

.autocomplete-result {
    list-style: none;
    text-align: left;
    padding: 4px 2px;
    cursor: pointer;
    background-color: white;
}

.autocomplete-result.is-active,
.autocomplete-result:hover {
    background-color: #ccc;
    color: white;
}
</style>