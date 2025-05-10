import { Widget } from '@lumino/widgets';
import { E2XMarkdownCell } from './cell';
import { ISignal, Signal } from '@lumino/signaling';
import { Token } from '@lumino/coreutils';

export type E2xRenderCellFunction = (
  widget: Widget,
  cell: E2XMarkdownCell
) => void;

export interface IE2xCellPlugin {
  cellType: string;
  label: string;
  renderCell: E2xRenderCellFunction;
  cleanMetadata: Record<string, any>;
}

export const IE2xCellPluginRegistry = new Token<IE2xCellPluginRegistry>(
  '@e2xgrader/cell-registry:IE2xCellPluginRegistry'
);

export interface IE2xCellPluginRegistry {
  registerCellPlugin(plugin: IE2xCellPlugin): void;
  getCellPlugin(cellType: string): IE2xCellPlugin | undefined;
  getCellPlugins(): IE2xCellPlugin[];
  getCellPluginLabel(cellType: string): string | undefined;
  getCellPluginTypes(): string[];
  cellPluginRegistered: ISignal<this, { plugin: IE2xCellPlugin }>;
}

export class E2xCellPluginRegistry implements IE2xCellPluginRegistry {
  private cellPlugins: { [key: string]: IE2xCellPlugin } = {};
  private readonly _cellPluginRegistered = new Signal<
    this,
    { plugin: IE2xCellPlugin }
  >(this);

  get cellPluginRegistered(): ISignal<this, { plugin: IE2xCellPlugin }> {
    return this._cellPluginRegistered;
  }

  registerCellPlugin(plugin: IE2xCellPlugin): void {
    if (this.cellPlugins[plugin.cellType]) {
      throw new Error(`Cell plugin ${plugin.cellType} is already registered.`);
    }
    this.cellPlugins[plugin.cellType] = plugin;
    this._cellPluginRegistered.emit({ plugin });
  }
  getCellPlugin(cellType: string): IE2xCellPlugin | undefined {
    return this.cellPlugins[cellType];
  }
  getCellPlugins(): IE2xCellPlugin[] {
    return Object.values(this.cellPlugins);
  }
  getCellPluginLabel(cellType: string): string | undefined {
    return this.cellPlugins[cellType]?.label;
  }
  getCellPluginTypes(): string[] {
    return Object.keys(this.cellPlugins);
  }
}
