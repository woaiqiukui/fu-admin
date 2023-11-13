<template>
    <PageWrapper title="项目名称：" + {{ project_name }} contentBackground>

    <template #extra>
      <a-button> 操作二 </a-button>
      <a-button type="primary"> 主操作 </a-button>
    </template>

    <template #footer>
      <a-tabs default-active-key="1">
        <a-tab-pane key="1" tab="任务情况汇总" />
        <a-tab-pane key="2" tab="端口信息" />
        <a-tab-pane key="3" tab="服务信息" />
        <a-tab-pane key="4" tab="指纹信息" />
        <a-tab-pane key="5" tab="弱口令信息" />
        <a-tab-pane key="6" tab="漏洞信息" />
      </a-tabs>
    </template>

    <div class="pt-4 m-4 desc-wrap">

</template>
