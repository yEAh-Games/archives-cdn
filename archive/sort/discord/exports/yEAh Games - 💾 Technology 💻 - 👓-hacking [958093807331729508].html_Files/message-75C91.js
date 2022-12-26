// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * T-Rex runner.
 * @param {string} outerContainerId Outer containing element id.
 * @param {!Object=} opt_config
 * @constructor
 * @implements {EventListener}
 * @export
 */
function Runner(outerContainerId, opt_config) {
  // Singleton
  if (Runner.instance_) {
    return Runner.instance_;
  }
  Runner.instance_ = this;

  this.outerContainerEl = document.querySelector(outerContainerId);
  this.containerEl = null;
  this.snackbarEl = null;
  // A div to intercept touch events. Only set while (playing && useTouch).
  this.touchController = null;

  this.config = opt_config || Object.assign(Runner.config, Runner.normalConfig);
  // Logical dimensions of the container.
  this.dimensions = Runner.defaultDimensions;

  this.gameType = null;
  Runner.spriteDefinition = Runner.spriteDefinitionByType['original'];

  this.altGameImageSprite = null;
  this.altGameModeActive = false;
  this.altGameModeFlashTimer = null;
  this.fadeInTimer = 0;

  this.canvas = null;
  this.canvasCtx = null;

  this.tRex = null;

  this.distanceMeter = null;
  this.distanceRan = 0;

  this.highestScore = 0;
  this.syncHighestScore = false;

  this.time = 0;
  this.runningTime = 0;
  this.msPerFrame = 1000 / FPS;
  this.currentSpeed = this.config.SPEED;
  Runner.slowDown = false;

  this.obstacles = [];

  this.activated = false; // Whether the easter egg has been activated.
  this.playing = false; // Whether the game is currently in play state.
  this.crashed = false;
  this.paused = false;
  this.inverted = false;
  this.invertTimer = 0;
  this.resizeTimerId_ = null;

  this.playCount = 0;

  // Sound FX.
  this.audioBuffer = null;

  /** @type {Object} */
  this.soundFx = {};
  this.generatedSoundFx = null;

  // Global web audio context for playing sounds.
  this.audioContext = null;

  // Images.
  this.images = {};
  this.imagesLoaded = 0;

  // Gamepad state.
  this.pollingGamepads = false;
  this.gamepadIndex = undefined;
  this.previousGamepad = null;

  if (this.isDisabled()) {
    this.setupDisabledRunner();
  } else {
    if (Runner.isAltGameModeEnabled()) {
      this.initAltGameType();
      Runner.gameType = this.gameType;
    }
    this.loadImages();

    window['initializeEasterEggHighScore'] =
        this.initializeHighScore.bind(this);
  }
}

/**
 * Default game width.
 * @const
 */
const DEFAULT_WIDTH = 600;

/**
 * Frames per second.
 * @const
 */
const FPS = 60;

/** @const */
const IS_HIDPI = window.devicePixelRatio > 1;

/** @const */
const IS_IOS = /CriOS/.test(window.navigator.userAgent);

/** @const */
const IS_MOBILE = /Android/.test(window.navigator.userAgent) || IS_IOS;

/** @const */
const IS_RTL = document.querySelector('html').dir == 'rtl';

/** @const */
const ARCADE_MODE_URL = 'chrome://dino/';

/** @const */
const RESOURCE_POSTFIX = 'offline-resources-';

/** @const */
const A11Y_STRINGS = {
  ariaLabel: 'dinoGameA11yAriaLabel',
  description: 'dinoGameA11yDescription',
  gameOver: 'dinoGameA11yGameOver',
  highScore: 'dinoGameA11yHighScore',
  jump: 'dinoGameA11yJump',
  started: 'dinoGameA11yStartGame',
  speedLabel: 'dinoGameA11ySpeedToggle'
};

/**
 * Default game configuration.
 * Shared config for all  versions of the game. Additional parameters are
 * defined in Runner.normalConfig and Runner.slowConfig.
 */
Runner.config = {
  AUDIOCUE_PROXIMITY_THRESHOLD: 190,
  AUDIOCUE_PROXIMITY_THRESHOLD_MOBILE_A11Y: 250,
  BG_CLOUD_SPEED: 0.2,
  BOTTOM_PAD: 10,
  // Scroll Y threshold at which the game can be activated.
  CANVAS_IN_VIEW_OFFSET: -10,
  CLEAR_TIME: 3000,
  CLOUD_FREQUENCY: 0.5,
  FADE_DURATION: 1,
  FLASH_DURATION: 1000,
  GAMEOVER_CLEAR_TIME: 1200,
  INITIAL_JUMP_VELOCITY: 12,
  INVERT_FADE_DURATION: 12000,
  MAX_BLINK_COUNT: 3,
  MAX_CLOUDS: 6,
  MAX_OBSTACLE_LENGTH: 3,
  MAX_OBSTACLE_DUPLICATION: 2,
  RESOURCE_TEMPLATE_ID: 'audio-resources',
  SPEED: 6,
  SPEED_DROP_COEFFICIENT: 3,
  ARCADE_MODE_INITIAL_TOP_POSITION: 35,
  ARCADE_MODE_TOP_POSITION_PERCENT: 0.1
};

Runner.normalConfig = {
  ACCELERATION: 0.001,
  AUDIOCUE_PROXIMITY_THRESHOLD: 190,
  AUDIOCUE_PROXIMITY_THRESHOLD_MOBILE_A11Y: 250,
  GAP_COEFFICIENT: 0.6,
  INVERT_DISTANCE: 700,
  MAX_SPEED: 13,
  MOBILE_SPEED_COEFFICIENT: 1.2,
  SPEED: 6
};


Runner.slowConfig = {
  ACCELERATION: 0.0005,
  AUDIOCUE_PROXIMITY_THRESHOLD: 170,
  AUDIOCUE_PROXIMITY_THRESHOLD_MOBILE_A11Y: 220,
  GAP_COEFFICIENT: 0.3,
  INVERT_DISTANCE: 350,
  MAX_SPEED: 9,
  MOBILE_SPEED_COEFFICIENT: 1.5,
  SPEED: 4.2
};


/**
 * Default dimensions.
 */
Runner.defaultDimensions = {
  WIDTH: DEFAULT_WIDTH,
  HEIGHT: 150
};


/**
 * CSS class names.
 * @enum {string}
 */
Runner.classes = {
  ARCADE_MODE: 'arcade-mode',
  CANVAS: 'runner-canvas',
  CONTAINER: 'runner-container',
  CRASHED: 'crashed',
  ICON: 'icon-offline',
  INVERTED: 'inverted',
  SNACKBAR: 'snackbar',
  SNACKBAR_SHOW: 'snackbar-show',
  TOUCH_CONTROLLER: 'controller'
};


/**
 * Sound FX. Reference to the ID of the audio tag on interstitial page.
 * @enum {string}
 */
Runner.sounds = {
  BUTTON_PRESS: 'offline-sound-press',
  HIT: 'offline-sound-hit',
  SCORE: 'offline-sound-reached'
};


/**
 * Key code mapping.
 * @enum {Object}
 */
Runner.keycodes = {
  JUMP: {'38': 1, '32': 1},  // Up, spacebar
  DUCK: {'40': 1},  // Down
  RESTART: {'13': 1}  // Enter
};


/**
 * Runner event names.
 * @enum {string}
 */
Runner.events = {
  ANIM_END: 'webkitAnimationEnd',
  CLICK: 'click',
  KEYDOWN: 'keydown',
  KEYUP: 'keyup',
  POINTERDOWN: 'pointerdown',
  POINTERUP: 'pointerup',
  RESIZE: 'resize',
  TOUCHEND: 'touchend',
  TOUCHSTART: 'touchstart',
  VISIBILITY: 'visibilitychange',
  BLUR: 'blur',
  FOCUS: 'focus',
  LOAD: 'load',
  GAMEPADCONNECTED: 'gamepadconnected',
};

Runner.prototype = {
  /**
   * Initialize alternative game type.
   */
  initAltGameType() {
    if (GAME_TYPE.length > 0) {
      this.gameType = loadTimeData && loadTimeData.valueExists('altGameType') ?
          GAME_TYPE[parseInt(loadTimeData.getValue('altGameType'), 10) - 1] :
          '';
    }
  },

  /**
   * Whether the easter egg has been disabled. CrOS enterprise enrolled devices.
   * @return {boolean}
   */
  isDisabled() {
    return loadTimeData && loadTimeData.valueExists('disabledEasterEgg');
  },

  /**
   * For disabled instances, set up a snackbar with the disabled message.
   */
  setupDisabledRunner() {
    this.containerEl = document.createElement('div');
    this.containerEl.className = Runner.classes.SNACKBAR;
    this.containerEl.textContent = loadTimeData.getValue('disabledEasterEgg');
    this.outerContainerEl.appendChild(this.containerEl);

    // Show notification when the activation key is pressed.
    document.addEventListener(Runner.events.KEYDOWN, function(e) {
      if (Runner.keycodes.JUMP[e.keyCode]) {
        this.containerEl.classList.add(Runner.classes.SNACKBAR_SHOW);
        document.querySelector('.icon').classList.add('icon-disabled');
      }
    }.bind(this));
  },

  /**
   * Setting individual settings for debugging.
   * @param {string} setting
   * @param {number|string} value
   */
  updateConfigSetting(setting, value) {
    if (setting in this.config && value !== undefined) {
      this.config[setting] = value;

      switch (setting) {
        case 'GRAVITY':
        case 'MIN_JUMP_HEIGHT':
        case 'SPEED_DROP_COEFFICIENT':
          this.tRex.config[setting] = value;
          break;
        case 'INITIAL_JUMP_VELOCITY':
          this.tRex.setJumpVelocity(value);
          break;
        case 'SPEED':
          this.setSpeed(/** @type {number} */ (value));
          break;
      }
    }
  },

  /**
   * Creates an on page image element from the base 64 encoded string source.
   * @param {string} resourceName Name in data object,
   * @return {HTMLImageElement} The created element.
   */
  createImageElement(resourceName) {
    const imgSrc = loadTimeData && loadTimeData.valueExists(resourceName) ?
        loadTimeData.getString(resourceName) :
        null;

    if (imgSrc) {
      const el =
          /** @type {HTMLImageElement} */ (document.createElement('img'));
      el.id = resourceName;
      el.src = imgSrc;
      document.getElementById('offline-resources').appendChild(el);
      return el;
    }
    return null;
  },

  /**
   * Cache the appropriate image sprite from the page and get the sprite sheet
   * definition.
   */
  loadImages() {
    let scale = '1x';
    this.spriteDef = Runner.spriteDefinition.LDPI;
    if (IS_HIDPI) {
      scale = '2x';
      this.spriteDef = Runner.spriteDefinition.HDPI;
    }

    Runner.imageSprite = /** @type {HTMLImageElement} */
        (document.getElementById(RESOURCE_POSTFIX + scale));

    if (this.gameType) {
      Runner.altGameImageSprite = /** @type {HTMLImageElement} */
          (this.createImageElement('altGameSpecificImage' + scale));
      Runner.altCommonImageSprite = /** @type {HTMLImageElement} */
          (this.createImageElement('altGameCommonImage' + scale));
    }
    Runner.origImageSprite = Runner.imageSprite;

    // Disable the alt game mode if the sprites can't be loaded.
    if (!Runner.altGameImageSprite || !Runner.altCommonImageSprite) {
      Runner.isAltGameModeEnabled = () => false;
      this.altGameModeActive = false;
    }

    if (Runner.imageSprite.complete) {
      this.init();
    } else {
      // If the images are not yet loaded, add a listener.
      Runner.imageSprite.addEventListener(Runner.events.LOAD,
          this.init.bind(this));
    }
  },

  /**
   * Load and decode base 64 encoded sounds.
   */
  loadSounds() {
    if (!IS_IOS) {
      this.audioContext = new AudioContext();

      const resourceTemplate =
          document.getElementById(this.config.RESOURCE_TEMPLATE_ID).content;

      for (const sound in Runner.sounds) {
        let soundSrc =
            resourceTemplate.getElementById(Runner.so…