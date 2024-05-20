<template>
    <div class="container">
      <div class="alert alert-success" role="alert">{{ message }}</div>
      <br/>
    </div>
  </template>
  
<script>
  export default {
    props: ['message'],
  };
</script>

<style scoped>
.container{
  position: absolute;
  margin-top: 10px;
  width: 85%;
  display: inline-grid;
}
.alert{
  height: 50px;
  margin-bottom: 0px;
  display: inline-block;
}
</style>