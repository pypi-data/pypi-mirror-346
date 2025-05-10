import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IEditorServices } from '@jupyterlab/codeeditor';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { NotebookPanel } from '@jupyterlab/notebook';
import { E2XContentFactory } from './factory';
import { IE2xCellPluginRegistry, E2xCellPluginRegistry } from './cellplugin';
import { choiceCellPlugins } from './plugins/choiceplugins';

const cellRegistryPlugin: JupyterFrontEndPlugin<IE2xCellPluginRegistry> = {
  id: '@e2xgrader/cell-registry:cell-registry',
  provides: IE2xCellPluginRegistry,
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log(
      'JupyterLab extension @e2xgrader/cell-registry:cell-registry is activated!'
    );
    const cellRegistry = new E2xCellPluginRegistry();
    app.serviceManager.ready.then(() => {
      console.log('Cell registry is ready.');
    });
    console.log('Cell registry created:', cellRegistry);
    choiceCellPlugins.forEach(plugin => {
      cellRegistry.registerCellPlugin(plugin);
    });
    return cellRegistry;
  }
};

const cellFactoryPlugin: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> =
  {
    id: '@e2xgrader/cell-registry:cell-factory',
    requires: [IEditorServices, IE2xCellPluginRegistry],
    optional: [ISettingRegistry],
    provides: NotebookPanel.IContentFactory,
    activate: async (
      _app: JupyterFrontEnd,
      editorServices: IEditorServices,
      cellRegistry: IE2xCellPluginRegistry,
      settingRegistry: ISettingRegistry | null
    ) => {
      console.log(
        'JupyterLab extension @e2xgrader/cell-registry:cell-factory is activated!'
      );
      const editorFactory = editorServices.factoryService.newInlineEditor;
      let contentFactory: E2XContentFactory;

      if (settingRegistry) {
        const settings = await settingRegistry.load(cellFactoryPlugin.id);
        contentFactory = new E2XContentFactory(
          { editorFactory },
          settings,
          cellRegistry
        );
      } else {
        contentFactory = new E2XContentFactory(
          {
            editorFactory
          },
          undefined,
          cellRegistry
        );
      }
      console.log('E2XContentFactory created:', contentFactory);
      return contentFactory;
    }
  };

export default [cellRegistryPlugin, cellFactoryPlugin];
