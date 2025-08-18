import { Frame } from '@nativescript/core';

export class NavigationService {
  public navigateTo(page: string) {
    Frame.topmost().navigate(page);
  }
}
