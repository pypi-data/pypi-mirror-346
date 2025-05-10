import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { LabIcon } from '@jupyterlab/ui-components';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import cellToolbarPlugin from './plugins/cell-toolbar';
import { JupytPanel } from './panel';

// Create the chat icon
const chatIcon = new LabIcon({
  name: 'jupyter-ai:chat',
  svgstr: `<svg xmlns="http://www.w3.org/2000/svg" width="16" viewBox="0 0 24 24">
      <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
    </svg>`
});

export namespace CommandIDs {
  /**
   * Command to toggle AI Chat sidebar visibility.
   */
  export const toggleAiChat = 'jupyter-ai:toggle-chat';
}

/**
 * Initialization data for the jupyt extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyt:plugin',
  autoStart: true,
  requires: [ICommandPalette, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settings: ISettingRegistry
  ) => {
    console.log('JupyterLab extension jupyt is activated!');

    const panel = new JupytPanel(app);
    panel.id = 'jupyt-panel';
    panel.title.label = 'Jupyt';
    panel.title.icon = chatIcon;
    panel.title.closable = true;

    app.shell.add(panel, 'right');

    const command = 'jupyt:open';
    app.commands.addCommand(command, {
      label: 'Open Jupyt',
      execute: () => {
        app.shell.activateById(panel.id);
        return null;
      }
    });

    palette.addItem({ command, category: 'Jupyt' });
  }
};

const plugins: JupyterFrontEndPlugin<any>[] = [plugin, cellToolbarPlugin];

export default plugins;
