import * as vscode from 'vscode';
import config from './config';

const COMMAND_ID_TOGGLE = 'codea.toggle-enable-status';

class CodeAStatusBar {
    private statusBarItemInstance_:vscode.StatusBarItem | null = null;

    initialize(context: vscode.ExtensionContext) {
        context.subscriptions.push(
            vscode.commands.registerCommand(COMMAND_ID_TOGGLE, () => {
                this.showToggleEnableStatusMessage(context);
            })
        );
        // create a new status bar item that we can now manage
        this.statusBarItemInstance_ = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
    
        this.statusBarItemInstance_.command = COMMAND_ID_TOGGLE;
        this.toggleEnableStatusTo(context, config.getEnableState(context));
    }

    async showToggleEnableStatusMessage(context: vscode.ExtensionContext) {
        if (config.getEnableState(context)) {
            const ret = await vscode.window.showInformationMessage(
                'Want to disable code generation and translation?',
                'Disable',
                'Cancel'
            );
            if (ret === 'Disable') {
                this.toggleEnableStatusTo(context, false);
            }
        } else {
            const ret = await vscode.window.showInformationMessage(
                'Want to enable code generation and translation?',
                'Enable',
                'Cancel'
            );
            if (ret === 'Enable') {
                this.toggleEnableStatusTo(context, true);
            }
        }
    }


    async toggleEnableStatusTo(context: vscode.ExtensionContext, newVal: boolean) {
        if(this.statusBarItemInstance_ === null) {
            console.log('Not initialized yet.');
            return;
        }
        await config.setEnable(newVal);
        context.globalState.update("enable", newVal);
        let bg: vscode.ThemeColor | string;
        let icon: string;
        if (newVal) {
            bg = "#7B5F00";
            icon = `$(extensions-sync-enabled)A+`;
        } else {
            bg = "#666666";
            icon = `$(extensions-sync-ignored)A+`;
        }
        this.statusBarItemInstance_.backgroundColor = bg;
        this.statusBarItemInstance_.text = icon;
        this.statusBarItemInstance_.show();
    }
}

const statusbaritem = new CodeAStatusBar();
export default statusbaritem;
