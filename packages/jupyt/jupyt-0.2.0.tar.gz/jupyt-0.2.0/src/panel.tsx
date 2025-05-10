import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Chat } from './components/chat';
import JupytSettings from './components/jupyt-settings';
import UserProfile from './components/user-profile';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { NotebookPanel } from '@jupyterlab/notebook';
import { ISessionContext } from '@jupyterlab/apputils';
import { Box, IconButton } from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { ThemeProvider } from './theme-provider';
import { CommandRegistry } from '@lumino/commands';

/**
 * JupytPanel
 * Main sidebar panel for Jupyt, now with tabs for Chat, Settings, and User Profile.
 */
export class JupytPanel extends ReactWidget {
  private app: JupyterFrontEnd;
  private _notebookPanel: NotebookPanel | undefined;
  private _sessionContext: ISessionContext | undefined;
  private commands: CommandRegistry;
  state: { 
    showSettings: boolean;
    showProfile: boolean;
  };

  constructor(app: JupyterFrontEnd) {
    super();
    this.app = app;
    this.commands = app.commands;
    this.addClass('jp-JupytPanel');
    this.node.style.position = 'relative';
    this.node.style.zIndex = '1000';
    this.state = { 
      showSettings: false,
      showProfile: false
    };
    this._updateNotebookPanel();
    const shell = this.app.shell;
    if (shell && shell.currentChanged) {
      shell.currentChanged.connect(this._onCurrentWidgetChanged, this);
    }
  }

  private _onCurrentWidgetChanged = (): void => {
    this._updateNotebookPanel();
  };

  private _updateNotebookPanel(): void {
    const shell = this.app.shell;
    if (!shell) {
      console.warn('Shell is not available');
      return;
    }
    const currentWidget = shell.currentWidget;
    let notebookPanel: NotebookPanel | undefined;
    if (currentWidget instanceof NotebookPanel) {
      notebookPanel = currentWidget;
    } else {
      const widgets = shell.widgets('main') || [];
      for (const widget of widgets) {
        if (widget instanceof NotebookPanel) {
          notebookPanel = widget;
          break;
        }
      }
    }
    const sessionContext = notebookPanel?.sessionContext;
    if (this._notebookPanel !== notebookPanel || this._sessionContext !== sessionContext) {
      this._notebookPanel = notebookPanel;
      this._sessionContext = sessionContext;
      this.update();
    }
  }

  dispose(): void {
    const shell = this.app.shell;
    if (shell && shell.currentChanged) {
      shell.currentChanged.disconnect(this._onCurrentWidgetChanged, this);
    }
    super.dispose();
  }

  private toggleSettings = () => {
    this.state = { 
      ...this.state, 
      showSettings: !this.state.showSettings,
      showProfile: false
    };
    this.update();
  };

  private toggleProfile = () => {
    this.state = { 
      ...this.state, 
      showProfile: !this.state.showProfile,
      showSettings: false
    };
    this.update();
  };

  render(): JSX.Element {
    const { showSettings, showProfile } = this.state;

    return (
      <ThemeProvider commands={this.commands}>
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
              padding: '4px 8px',
              borderBottom: '1px solid var(--jp-border-color1)'
            }}
          >
            <IconButton 
              onClick={this.toggleProfile} 
              size="small" 
              title="User Profile"
              sx={{ mr: 1 }}
            >
              <AccountCircleIcon fontSize="small" />
            </IconButton>
            <IconButton onClick={this.toggleSettings} size="small" title="Settings">
              <SettingsIcon fontSize="small" />
            </IconButton>
          </Box>

          <Box sx={{ flex: 1, overflow: 'auto', position: 'relative' }}>
            {showSettings ? (
              <JupytSettings />
            ) : showProfile ? (
              <UserProfile />
            ) : (
              <Chat notebookPanel={this._notebookPanel} sessionContext={this._sessionContext} />
            )}
          </Box>
        </Box>
      </ThemeProvider>
    );
  }
} 