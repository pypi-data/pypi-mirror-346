import { IE2xCellPlugin } from '../cellplugin';

import { Widget } from '@lumino/widgets';
import { E2XMarkdownCell } from '../cell';

export namespace ChoiceCellUtils {
  export function get_choices(cell: E2XMarkdownCell): string[] {
    return cell.getE2xMetadataField('choice') ?? [];
  }

  export function set_choices(cell: E2XMarkdownCell, choices: string[]): void {
    cell.setE2xMetadataField('choice', choices);
  }

  export function add_choice(cell: E2XMarkdownCell, choice: string): void {
    const choices = get_choices(cell);
    if (!choices.includes(choice)) {
      choices.push(choice);
      set_choices(cell, choices);
    }
  }
  export function remove_choice(cell: E2XMarkdownCell, choice: string): void {
    const choices = get_choices(cell);
    const index = choices.indexOf(choice);
    if (index !== -1) {
      choices.splice(index, 1);
      set_choices(cell, choices);
    }
  }

  export function get_choice_count(cell: E2XMarkdownCell): number {
    return cell.getE2xMetadataField('num_of_choices') ?? 0;
  }
  export function set_choice_count(cell: E2XMarkdownCell, count: number): void {
    cell.setE2xMetadataField('num_of_choices', count);
  }

  export function get_choice(cell: E2XMarkdownCell): string {
    return cell.getE2xMetadataField('choice') ?? '';
  }

  export function set_choice(cell: E2XMarkdownCell, choice: string): void {
    cell.setE2xMetadataField('choice', choice);
  }
}

export namespace MultipleChoice {
  export const E2X_MULTIPLECHOICE_CELL_TYPE = 'multiplechoice';
  export const E2X_MULTIPLECHOICE_FORM_CLASS = 'e2x-multiplechoice-form';

  export const cleanMetadata = {
    choice: [] as string[],
    num_of_choices: 0,
    type: E2X_MULTIPLECHOICE_CELL_TYPE
  } as Record<string, any>;

  export function createChoiceElement(
    cell: E2XMarkdownCell,
    value: string,
    selected: boolean
  ): HTMLInputElement {
    const choice = document.createElement('input');
    choice.type = 'checkbox';
    choice.name = cell.model.id;
    choice.value = value;
    choice.checked = selected;
    choice.onchange = event => {
      const elem = event.target as HTMLInputElement;
      if (elem.checked) {
        ChoiceCellUtils.add_choice(cell, value);
      } else {
        ChoiceCellUtils.remove_choice(cell, value);
      }
    };
    return choice;
  }

  export function renderCell(widget: Widget, cell: E2XMarkdownCell): void {
    console.log('Rendering MC cell:', cell);
    const html = widget.node;
    const lists = html.querySelectorAll('ul');
    if (lists.length === 0) {
      return;
    }
    const list = lists[0];
    const items = list.querySelectorAll('li');
    const form = document.createElement('form');
    form.classList.add(E2X_MULTIPLECHOICE_FORM_CLASS);
    if (ChoiceCellUtils.get_choice_count(cell) !== items.length) {
      ChoiceCellUtils.set_choice_count(cell, items.length);
      ChoiceCellUtils.set_choices(cell, []);
    }
    const choices = ChoiceCellUtils.get_choices(cell);
    items.forEach((item, index) => {
      const input = createChoiceElement(
        cell,
        index.toString(),
        choices.includes(index.toString())
      );
      const label = document.createElement('label');
      label.innerHTML = item.innerHTML;
      form.appendChild(input);
      form.appendChild(label);
      form.appendChild(document.createElement('br'));
    });
    list.replaceWith(form);
  }

  export const cellPlugin: IE2xCellPlugin = {
    cellType: E2X_MULTIPLECHOICE_CELL_TYPE,
    label: 'Multiple Choice',
    renderCell: renderCell,
    cleanMetadata: cleanMetadata
  };
}

export namespace SingleChoice {
  export const E2X_SINGLECHOICE_CELL_TYPE = 'singlechoice';
  export const E2X_SINGLECHOICE_FORM_CLASS = 'e2x-singlechoice-form';
  export const cleanMetadata = {
    choice: '' as string,
    type: E2X_SINGLECHOICE_CELL_TYPE
  } as Record<string, any>;

  export function createChoiceElement(
    cell: E2XMarkdownCell,
    value: string,
    selected: boolean
  ): HTMLInputElement {
    const choice = document.createElement('input');
    choice.type = 'radio';
    choice.name = cell.model.id;
    choice.value = value;
    choice.checked = selected;
    choice.onchange = event => {
      const elem = event.target as HTMLInputElement;
      if (elem.checked) {
        ChoiceCellUtils.set_choice(cell, value);
      }
    };
    return choice;
  }

  export function renderCell(widget: Widget, cell: E2XMarkdownCell): void {
    console.log('Rendering SC cell:', cell);
    const html = widget.node;
    const lists = html.querySelectorAll('ul');
    if (lists.length === 0) {
      return;
    }
    const list = lists[0];
    const items = list.querySelectorAll('li');
    const form = document.createElement('form');
    form.classList.add(E2X_SINGLECHOICE_FORM_CLASS);
    const choice = ChoiceCellUtils.get_choice(cell);
    if (choice !== '' && parseInt(choice) >= items.length) {
      ChoiceCellUtils.set_choice(cell, '');
    }
    items.forEach((item, index) => {
      const input = createChoiceElement(
        cell,
        index.toString(),
        choice === index.toString()
      );
      const label = document.createElement('label');
      label.innerHTML = item.innerHTML;
      form.appendChild(input);
      form.appendChild(label);
      form.appendChild(document.createElement('br'));
    });
    list.replaceWith(form);
  }
  export const cellPlugin: IE2xCellPlugin = {
    cellType: E2X_SINGLECHOICE_CELL_TYPE,
    label: 'Single Choice',
    renderCell: renderCell,
    cleanMetadata: cleanMetadata
  };
}

export const choiceCellPlugins = [
  MultipleChoice.cellPlugin,
  SingleChoice.cellPlugin
];
