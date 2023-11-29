<template>
  <div class="table-container">
    <a-table
      :columns="columns"
      :dataSource="secInfoList"
      rowKey="url"
      class="secinfo-table"
      @row-click="handleRowClick"
    />
  </div>
</template>

<script lang="tsx">
  import { defineComponent } from 'vue';
  import { Table, Tag } from 'ant-design-vue';
  import { Button } from '/@/components/Button';

  export default defineComponent({
    name: 'SecInfoTable',
    components: {
      [Table.name]: Table,
      [Table.Column.name]: Table.Column,
      [Tag.name]: Tag,
    },
    props: {
      secInfoList: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        columns: [
          {
            title: '时间',
            dataIndex: 'timestamp',
            key: 'timestamp',
            class: 'timestamp-cell',
          },
          {
            title: '主题',
            dataIndex: 'subject',
            key: 'subject',
            class: 'subject-cell',
            customRender: ({ record }) => {
              return (
                <Button
                  type="link"
                  size="small"
                  href={record.url}
                  title={record.subject}
                  class="subject-cell-link"
                >
                  {() => record.subject}
                </Button>
              );
            },
          },
          {
            title: '内容',
            dataIndex: 'content',
            key: 'content',
            class: 'content-cell',
            customRender: ({ record }) => {
              return <span title={record.content}>{record.content}</span>;
            },
          },
          {
            title: '标签',
            dataIndex: 'label',
            key: 'label',
            class: 'label-cell',
          },
        ],
      };
    },
    methods: {
      handleRowClick(record) {
        // Handle row click event
        console.log('Row clicked:', record);
      },
    },
  });
</script>

<style>
  .table-container {
    width: 100%;
    overflow-x: auto;
  }

  .secinfo-table {
    width: 100%;
    margin-bottom: 20px;
  }

  .timestamp-cell,
  .label-cell,
  .subject-cell,
  .content-cell {
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .timestamp-cell {
    min-width: 170px;
  }

  .subject-cell-link {
    display: block;
  }
</style>
