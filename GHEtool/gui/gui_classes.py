"""
GUI classes which can be used in the gui_structure.py file.

There are three types of objects that can be put on the GUI.

1) Structural objects
    Page, Aim and Category (provide some structuring to the GUI)
2) Options
    FloatBox, IntegerBox, ButtonBox, ListBox, Filename, FunctionButton and Hint
3) Result elements
    ResultFigure and ResultText (related to the results page)

"""

from __future__ import annotations

import abc
from functools import partial as ft_partial
from typing import Callable, List, Optional, Union, Tuple
from os.path import exists

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

from GHEtool.gui.gui_base_class import DARK, GREY, LIGHT, LIGHT_SELECT, WARNING, WHITE


def _update_opponent_not_change(button: QtW.QPushButton, false_button_list: List[QtW.QPushButton] = None):
    """
    This function controls the behaviour of the buttons.
    This function makes sure that whenever a button is active, all other buttons except the current one,
    are inactive. If the current button is already active, nothing changes.

    Parameters
    ----------
    button : QtW.QPushButton
        Button which is activated (or pressed on)
    false_button_list : List[QtW.QPushButton]
        List with other buttons which aren't active

    Returns
    -------
    None
    """
    if not button.isChecked():
        button.setChecked(True)
        return
    for but in false_button_list:
        if not but == button:
            but.setChecked(False)


def _update_opponent_toggle(button: QtW.QPushButton, button_opponent: QtW.QPushButton, false_button_list: List[QtW.QPushButton] = None):
    """
    This function controls the behaviour of the buttons, specifically the toggle behaviour.
    This function makes sure that whenever a button is pressed, all other buttons except the current one,
    are inactive. If the current button is already active and it is still pressed, the current button
    is turned inactive and the button_opponent is made active.

    Parameters
    ----------
    button : QtW.QPushButton
        Button which is activated (iff it was not already), and which is deactivated if it was active and is pressed on
    button_opponent : QtW.QPushButton
        Button which is activated if the current button was active and is pressed on
    false_button_list : List[QtW.QPushButton]
        List with other buttons which aren't active

    Returns
    -------
    None
    """
    button_opponent.setChecked(not button.isChecked())
    if false_button_list is not None:
        for false_button in false_button_list:
            false_button.setChecked(False)


class Option(metaclass=abc.ABCMeta):
    """
    Abstract base class for a gui option.
    """

    default_parent: Optional[QtW.QWidget] = None

    def __init__(self, label: str, default_value: Union[bool, int, float, str], category: Category):
        """
        Parameters
        ----------
        label : str
            The label related to the option
        default_value : bool, int, float, str
            The default value of the option
        category : Category
            The category in which the option should be placed
        """
        self.label_text: str = label
        self.default_value: Union[bool, int, float, str] = default_value
        self.widget: Optional[QtW.QWidget] = None
        self.frame: QtW.QFrame = QtW.QFrame(self.default_parent)
        self.label = QtW.QLabel(self.frame)
        self.linked_options: List[(Option, int)] = []
        self.limit_size: bool = True
        category.list_of_options.append(self)
        self.list_2_check_before_value: List[Tuple[Option, int], Aim] = []

    @abc.abstractmethod
    def get_value(self) -> Union[bool, int, float, str]:
        """
        This function gets the value of the option.

        Returns
        -------
        The value of the option, either a bool, int, float or str
        """

    @abc.abstractmethod
    def set_value(self, value: Union[bool, int, float, str]) -> None:
        """
        This function sets the value of the option.

        Parameters
        ----------
        value : bool, int, float, str
            The value to which the option should be set.

        Returns
        -------
        None
        """

    @abc.abstractmethod
    def _check_value(self) -> bool:
        """
        Abstract function to check whether or not the current value of the option is a valid value.

        Returns
        -------
        bool
            True if the option value is valid
        """

    def add_aim_option_2_be_set_for_check(self, aim_or_option: Union[Tuple[Option, int], Aim]):
        """
        Sometimes, an option should not be check on its valid value. This can be the case when,
        for a specific aim or in a specific case, the current option is not needed. (e.g.,
        the FileNameBox should only be checked whenever an aim is chosen which requires a
        filename).
        This function adds a list of dependencies to the current object, which will be checked
        (meaning: it will be checked if their value is correct) before the value of the self-option
        will be checked.

        Parameters
        ----------
        aim_or_option : aim, (option, int)
            aim or option (with its corresponding index)

        Returns
        -------
        None
        """
        self.list_2_check_before_value.append(aim_or_option)

    def check_value(self) -> bool:
        """
        This function check whether the value of the option is valid.
        Before it checks the value, it makes sure to check all the dependencies in list_2_check_before_value.
        If the check of one of the aims or options in this list is True, True is returned.
        Otherwise the value of the current option is checked.

        Returns
        -------
        bool
            True if the value of the current option is valid.
        """
        if self.frame.isEnabled():
            if not self.list_2_check_before_value:
                return self._check_value()
            if any(aim.widget.isChecked() for aim in self.list_2_check_before_value if isinstance(aim, Aim)) or any(
                    value[0].get_value() == value[1] for value in self.list_2_check_before_value if isinstance(value, tuple)):
                return self._check_value()
        return True

    @abc.abstractmethod
    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout, *, row: int = None, column: int = None) -> None:
        """
        This functions creates the widget, related to the current object, in the frame.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which the widget should be created
        layout_parent : QtW.QLayout
            The parent layout of the current widget
        row : int
            The index of the row in which the widget should be created
            (only needed when there is a grid layout)
        column : int
            The index of the column in which the widget should be created
            (only needed when there is a grid layout)

        Returns
        -------
        None
        """

    @abc.abstractmethod
    def _init_links(self) -> None:
        """
        Abstract function on how the links for this particular object should be set.

        Returns
        -------
        None
        """

    def init_links(self) -> None:
        """
        This function initiates the links.

        Returns
        -------
        None
        """
        if self.linked_options:
            self._init_links()

    def set_text(self, name: str) -> None:
        """
        This function sets the label text

        Parameters
        ----------
        name : str
            Label name of the object

        Returns
        -------
        None
        """
        self.label_text = name
        self.label.setText(name)

    def deactivate_size_limit(self) -> None:
        """
        This function sets the size limit to False.

        Returns
        -------
        None
        """
        self.limit_size = False

    def create_frame(self, frame: QtW.QFrame, layout_parent: QtW.QLayout, create_spacer: bool = True) -> QtW.QHBoxLayout:
        """
        This function creates the frame for this option in a given frame (can be a page or category).
        If the current label text is "", then the frame attribute is set to the given frame.

        Parameters
        ----------
        frame : QtW.QFrame
            Frame in which this option should be created
        layout_parent : QtW.QLayout
            The layout parent of the current frame
        create_spacer : bool
            True if a spacer should be made

        Returns
        -------
        QtW.QHBoxLayout
            The frame created for this option
        """

        if self.label_text == "":
            self.frame.setParent(None)
            self.frame = frame
            return frame.layout()
        self.frame.setParent(frame)
        self.frame.setFrameShape(QtW.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtW.QFrame.Raised)
        self.frame.setStyleSheet("QFrame {\n" f"	border: 0px solid {WHITE};\n" "	border-radius: 0px;\n" "  }\n")
        layout = QtW.QHBoxLayout(self.frame)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label.setParent(frame)
        self.label.setText(self.label_text)
        layout.addWidget(self.label)
        if create_spacer:
            spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
            layout.addItem(spacer)
        layout_parent.addWidget(self.frame)
        return layout

    def hide(self) -> None:
        """
        This function makes the current frame invisible.

        Returns
        -------
        None
        """
        self.frame.hide()
        self.frame.setEnabled(False)

    def is_hidden(self) -> bool:
        """
        This function returns a boolean value related to whether or not the option is hidden.

        Returns
        -------
        Bool
            True if the option is hidden
        """
        return self.frame.isHidden()

    def show(self) -> None:
        """
        This function makes the current frame visible.

        Returns
        -------
        None
        """
        self.frame.show()
        self.frame.setEnabled(True)

    @abc.abstractmethod
    def change_event(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the option is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """

    def __repr__(self):
        return f'{type(self).__name__}; Label: {self.label_text}; Value: {self.get_value()}'

    def __str__(self):
        return self.__repr__


def check(linked_options: List[(Union[Option, List[Option]], int)], option_input: Option, index: int):
    """
    This function makes sure that the linked_options will be hidden when the index of the option_input
    is different from the index provided per Option in the linked_options list.
    When it is equal, the linked_option is shown.

    Parameters
    ----------
    linked_options : List[(Options, int) or  (List[Options], int)]
        List with linked option, composed of either an Option-index pair or a list of options-index pair
    option_input : Option
        The option which determines the visibility of the linked_options
    index : int
        The index which determines the visibility of the linked_options

    Returns
    -------
    None
    """
    index = index if option_input.get_value() == index else option_input.get_value()
    list_false = [(option, idx) for option, idx in linked_options if idx != index]
    list_true = [(option, idx) for option, idx in linked_options if idx == index]
    for option, idx in list_false:
        if isinstance(option, list):
            for opt in option:
                opt.hide()
            continue
        option.hide()
    for option, idx in list_true:
        if isinstance(option, list):
            for opt in option:
                opt.show()
            continue
        option.show()


class FloatBox(Option):
    """
    This class contains all the functionalities of the FloatBox option in the GUI.
    The FloatBox can be used to input floating point numbers.
    """
    def __init__(self, label: str, default_value: float, category: Category, decimal_number: int = 0,
                 minimal_value: float = 0.0, maximal_value: float = 100.0, step: float = 1.0):
        """

        Parameters
        ----------
        label : str
            The label of the FloatBox
        default_value : float
            The default value of the FloatBox
        category : Category
            Category in which the FloatBox should be placed
        decimal_number : int
            Number of decimal points in the FloatBox
        minimal_value : float
            Minimal value of the FloatBox
        maximal_value : float
            Maximal value of the FloatBox
        step : float
            The step by which the value of the FloatBox should change when the
            increase or decrease buttons are pressed.

        Examples
        --------
        >>> option_float = FloatBox(label='Float label text',
        >>>                         default_value=0.5,
        >>>                         category=category_example,
        >>>                         decimal_number=2,
        >>>                         minimal_value=0,
        >>>                         maximal_value=1,
        >>>                         step=0.1)

        Gives:

        .. figure:: _static/Example_Float_Box.PNG

        """
        super().__init__(label, default_value, category)
        self.decimal_number: int = decimal_number
        self.minimal_value: float = minimal_value
        self.maximal_value: float = maximal_value
        self.step: float = step
        self.widget: QtW.QDoubleSpinBox = QtW.QDoubleSpinBox(self.default_parent)

    def get_value(self) -> float:
        """
        This function gets the value of the FloatBox.

        Returns
        -------
        float
            Value of the FloatBox
        """
        return self.widget.value()

    def set_value(self, value: float) -> None:
        """
        This function sets the value of the FloatBox.

        Parameters
        ----------
        value : float
            Value to which the FloatBox should be set.

        Returns
        -------
        None
        """
        self.widget.setValue(value)

    def _init_links(self) -> None:
        """
        Function on how the links for the FloatBox should be set.

        Returns
        -------
        None
        """
        current_value: float = self.get_value()
        self.set_value(current_value*1.1)
        self.set_value(current_value)

    def _check_value(self) -> bool:
        """
        This function checks if the value of the FloatBox is between the minimal_value
        and maximal_value.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal value
        """
        return self.minimal_value <= self.get_value() <= self.maximal_value

    def add_link_2_show(self, option: Union[Option, Category, FunctionButton, Hint], below: float = None, above: float = None) -> None:
        """
        This function couples the visibility of an option to the value of the FloatBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.
        below : float
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : float
            Higher threshold of the FloatBox value above which the linked option will be hidden

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the FloatBox value to other options, hints, function buttons or categories.
        In the example below, 'option linked' will be shown if the float value is below 0.1 or above 0.9.

        >>> option_float.add_link_2_show(option=option_linked, below=0.1, above=0.9)
        """

        self.widget.valueChanged.connect(ft_partial(self.show_option, option, below=below, above=above))

    def show_option(self, option: Union[Option, Category, FunctionButton, Hint], below: Optional[float], above: Optional[float]):
        """
        This function shows the option if the value of the FloatBox is between the below and above value.
        If no below or above values are given, no boundary is taken into account for respectively the lower and
        upper boundary.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option to be shown or hidden
        below : float (optional)
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : float (optional)
            Higher threshold of the FloatBox value above which the linked option will be hidden

        Returns
        -------
        None
        """
        if below is not None and self.get_value() < below:
            return option.show()
        if above is not None and self.get_value() > above:
            return option.show()
        option.hide()

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the FloatBox is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """
        self.widget.valueChanged.connect(function_to_be_called)  # pylint: disable=E1101

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout, *, row: int = None, column: int = None) -> None:
        """
        This functions creates the FloatBox widget in the frame.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which the widget should be created
        layout_parent : QtW.QLayout
            The parent layout of the current widget
        row : int
            The index of the row in which the widget should be created
            (only needed when there is a grid layout)
        column : int
            The index of the column in which the widget should be created
            (only needed when there is a grid layout)

        Returns
        -------
        None
        """
        layout = self.create_frame(frame, layout_parent)
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f'QDoubleSpinBox{"{"}selection-color: {WHITE};selection-background-color: {LIGHT};border: 1px solid {WHITE};font: 11pt "Lexend Deca Light";{"}"}'
        )
        self.widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
        self.widget.setProperty("showGroupSeparator", True)
        self.widget.setMinimum(self.minimal_value)
        self.widget.setMaximum(self.maximal_value)
        self.widget.setDecimals(self.decimal_number)
        self.widget.setValue(self.default_value)
        self.widget.setSingleStep(self.step)
        if self.limit_size:
            self.widget.setMaximumWidth(100)
            self.widget.setMinimumWidth(100)
        self.widget.setMinimumHeight(28)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)


class IntBox(Option):
    """
    This class contains all the functionalities of the IntBox (integer box) option in the GUI.
    The IntBox can be used to input integer numbers.
    """
    def __init__(self, label: str, default_value: int, category: Category, minimal_value: int = 0, maximal_value: int = 100, step: int = 1):
        """

        Parameters
        ----------
        label : str
            The label of the IntBox
        default_value : int
            The default value of the IntBox
        category : Category
            Category in which the IntBox should be placed
        minimal_value : int
            Minimal value of the IntBox
        maximal_value : int
            Maximal value of the IntBox
        step : int
            The step by which the value of the IntBox should change when the
            increase or decrease buttons are pressed.

        Examples
        --------
        >>> option_float = IntBox(label='Int label text',
        >>>                       default_value=2,
        >>>                       category=category_example,
        >>>                       minimal_value=0,
        >>>                       maximal_value=12,
        >>>                       step=2)

        Gives:

        .. figure:: _static/Example_Int_Box.PNG

        """
        super().__init__(label, default_value, category)
        self.minimal_value: int = minimal_value
        self.maximal_value: int = maximal_value
        self.step: int = step
        self.widget: QtW.QSpinBox = QtW.QSpinBox(self.default_parent)

    def get_value(self) -> int:
        """
        This function gets the value of the IntBox.

        Returns
        -------
        int
            Value of the IntBox
        """
        return self.widget.value()

    def set_value(self, value: int) -> None:
        """
        This function sets the value of the IntBox.

        Parameters
        ----------
        value : int
            Value to which the IntBox should be set.

        Returns
        -------
        None
        """
        self.widget.setValue(value)

    def _init_links(self) -> None:
        """
        Function on how the links for the IntBox should be set.

        Returns
        -------
        None
        """
        current_value: int = self.get_value()
        self.set_value(self.minimal_value if current_value == self.minimal_value else self.minimal_value)
        self.set_value(current_value)

    def _check_value(self) -> bool:
        """
        This function checks if the value of the IntBox is between the minimal_value
        and maximal_value.

        Returns
        -------
        bool
            True if the value is between the minimal and maximal value
        """
        return self.minimal_value <= self.get_value() <= self.maximal_value

    def add_link_2_show(self, option: Union[Option, Category, FunctionButton, Hint], *, below: int = None, above: int = None):
        """
        This function couples the visibility of an option to the value of the IntBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the IntBox.
        below : float
            Lower threshold of the FloatBox value below which the linked option will be hidden
        above : float
            Higher threshold of the FloatBox value above which the linked option will be hidden

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the IntBox value to other options, hints, function buttons or categories.
        So in the example `option_linked` will be shown if the integer value is below 1 or above 10.

        >>> option_int.add_link_2_show(option=option_linked, below=1, above=10)
        """
        self.widget.valueChanged.connect(ft_partial(self.show_option, option, below=below, above=above))

    def show_option(self, option: Union[Option, Category, FunctionButton, Hint], below: Optional[int], above: Optional[int]):
        """
        This function shows the option if the value of the IntBox is between the below and above value.
        If no below or above values are given, no boundary is taken into account for respectively the lower and
        upper boundary.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option to be shown or hidden
        below : float (optional)
            Lower threshold of the IntBox value below which the linked option will be hidden
        above : float (optional)
            Higher threshold of the IntBox value above which the linked option will be hidden

        Returns
        -------
        None
        """
        if below is not None and self.get_value() < below:
            return option.show()
        if above is not None and self.get_value() > above:
            return option.show()
        option.hide()

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the IntBox is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """
        self.widget.valueChanged.connect(function_to_be_called)  # pylint: disable=E1101

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout,  *, row: int = None, column: int = None) -> None:
        """
        This functions creates the IntBox widget in the frame.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which the widget should be created
        layout_parent : QtW.QLayout
            The parent layout of the current widget
        row : int
            The index of the row in which the widget should be created
            (only needed when there is a grid layout)
        column : int
            The index of the column in which the widget should be created
            (only needed when there is a grid layout)

        Returns
        -------
        None
        """
        layout = self.create_frame(frame, layout_parent)
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f'QSpinBox{"{"}selection-color: {WHITE};selection-background-color: {LIGHT};border: 1px solid {WHITE};font: 11pt "Lexend Deca Light";{"}"}'
        )
        self.widget.setAlignment(QtC.Qt.AlignRight | QtC.Qt.AlignTrailing | QtC.Qt.AlignVCenter)
        self.widget.setMinimum(self.minimal_value)
        self.widget.setMaximum(self.maximal_value)
        self.widget.setValue(self.default_value)
        self.widget.setSingleStep(self.step)
        self.widget.setMaximumWidth(100)
        self.widget.setMinimumWidth(100)
        self.widget.setMinimumHeight(28)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)


class ButtonBox(Option):
    """
    This class contains all the functionalities of the ButtonBox option in the GUI.
    The ButtonBox can be used to input floating point numbers.
    """

    TOGGLE: bool = True

    def __init__(self, label: str, default_index: int, entries: List[str], category: Category):
        """

        Parameters
        ----------
        label : str
            The label of the ButtonBox
        default_index : int
            The default index of the ButtonBox
        entries : List[str]
            The list of all the different buttons in the ButtonBox
        category : Category
            Category in which the ButtonBox should be placed

        Examples
        --------
        >>> option_buttons = ButtonBox(label='Button box label text',
        >>>                            default_index=0,
        >>>                            entries=['option 1', 'option 2'],
        >>>                            category=category_example)

        Gives:

        .. figure:: _static/Example_Button_Box.PNG

        """
        super().__init__(label, default_index, category)
        self.entries: List[str] = entries
        self.widget: List[QtW.QPushButton] = [QtW.QPushButton(self.default_parent) for _ in self.entries]
        for idx, button in enumerate(self.widget):
            default_value = self.default_value if idx != self.default_value else idx - 1 if idx > 0 else 1
            button.clicked.connect(
                ft_partial(self.update_function, *(button, self.widget[default_value], [but for but in self.widget if but not in [
                    button, self.widget[default_value]]]))
            )
            button.clicked.connect(ft_partial(check, self.linked_options, self, self.get_value()))

    def get_value(self) -> int:
        """
        This function gets the value of the ButtonBox.

        Returns
        -------
        int
            Value of the ButtonBox
        """
        for idx, button in enumerate(self.widget):
            if button.isChecked():
                return idx
        return -1

    def set_value(self, value: int) -> None:
        """
        This function sets the value of the ButtonBox.

        Parameters
        ----------
        value : int
            Value to which the ButtonBox should be set.

        Returns
        -------
        None
        """
        button = self.widget[value]
        if not button.isChecked():
            button.click()

    def _init_links(self) -> None:
        """
        Function on how the links for the ButtonBox should be set.

        Returns
        -------
        None
        """
        current_value: int = self.get_value()
        self.set_value(0 if current_value != 0 else 1)
        self.set_value(current_value)

    def _check_value(self) -> bool:
        """
        This function checks whether or not at least one button is checked.

        Returns
        -------
        bool
            True if at least one button is checked. False otherwise
        """
        return any(button.isChecked() for button in self.widget)

    def add_link_2_show(self, option: Union[Option, Category, FunctionButton, Hint], on_index: int):
        """
        This function couples the visibility of an option to the value of the ButtonBox object.

        Parameters
        ----------
        option : Option, Category, FunctionButton, Hint
            Option which visibility should be linked to the value of the FloatBox.
        on_index : int
            The index on which the linked options should be made visible.

        Returns
        -------
        None

        Examples
        --------
        This function can be used to couple the ButtonBox value to other options, hints, function buttons or categories.
        In the example below, 'option linked' will be shown if the first ('0') option is selected in the ButtonBox.

        >>> option_buttons.add_link_2_show(option=option_linked, on_index=0)
        """

        self.linked_options.append([option, on_index])

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        This function calls the function_to_be_called whenever the ButtonBox is changed.

        Parameters
        ----------
        function_to_be_called : callable
            Function which should be called

        Returns
        -------
        None
        """
        for button in self.widget:
            button.clicked.connect(function_to_be_called)  # pylint: disable=E1101

    def set_text(self, name: str) -> None:
        """
        This function sets the text of the label and of the different buttons in the ButtonBox.

        Parameters
        ----------
        name: str
            String with the names of all the buttons (in order) and the label name at position 0.
            These strings are separated by ","

        Returns
        -------
        None
        """
        entry_name: List[str, str] = name.split(',')
        self.label_text = entry_name[0]
        self.label.setText(self.label_text)
        for button, button_name in zip(self.widget, entry_name[1:]):
            button.setText(f" {button_name.replace('++', ',')} ")

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout, row: int = None, column: int = None) -> None:
        """
        This functions creates the buttonBox widget in the frame.

        Parameters
        ----------
        frame : QtW.QFrame
            The frame object in which the widget should be created
        layout_parent : QtW.QLayout
            The parent layout of the current widget
        row : int
            The index of the row in which the widget should be created
            (only needed when there is a grid layout)
        column : int
            The index of the column in which the widget should be created
            (only needed when there is a grid layout)

        Returns
        -------
        None
        """
        layout = self.create_frame(frame, layout_parent)
        for idx, (entry, widget) in enumerate(zip(self.entries, self.widget)):
            widget.setParent(self.frame)
            widget.setText(f" {entry} ")
            widget.setStyleSheet(
                f"QPushButton{'{'}border: 3px solid {DARK};border-radius: 5px;gridline-color: {LIGHT};background-color: {GREY};font-weight:500;{'}'}"
                f"QPushButton:hover{'{'}border: 3px solid {DARK};background-color:{LIGHT};{'}'}"
                f"QPushButton:checked{'{'}border:3px solid {LIGHT};background-color:{LIGHT};{'}'}\n"
                f"QPushButton:disabled{'{'}border: 3px solid {GREY};border-radius: 5px;color: {WHITE};gridline-color: {GREY};background-color: {GREY};{'}'}\n"
                f"QPushButton:disabled:hover{'{'}background-color: {DARK};{'}'}"
            )
            widget.setCheckable(True)
            widget.setChecked(idx == self.default_value)
            widget.setMinimumHeight(30)
            layout.addWidget(widget)

    def update_function(self, button: QtW.QPushButton, button_opponent: QtW.QPushButton, false_button_list: List[QtW.QPushButton] = None) -> None:
        """
        This function updates which button should be checked/activated or unchecked/deactivated
        This can be done by either the toggle behaviour or not-change behaviour.

        Parameters
        ----------
        button : QtW.QPushButton
            Button which is activated (iff it was not already), and which is deactivated if it was active and is pressed on
        button_opponent : QtW.QPushButton
            Button which is activated if the current button was active and is pressed on
        false_button_list : List[QtW.QPushButton]
            List with other buttons which aren't active

        Returns
        -------
        None
        """
        if self.TOGGLE:
            _update_opponent_toggle(button, button_opponent, false_button_list)
            return
        _update_opponent_not_change(button, false_button_list + [button_opponent])


class ListBox(Option):
    """
    List input box\n
    """
    def __init__(self, label: str, default_index: int, entries: List[str], *, category: Category):
        super().__init__(label, default_index, category)
        self.entries: List[str] = entries
        self.widget: QtW.QComboBox = QtW.QComboBox(self.default_parent)

    def get_text(self) -> str:
        return self.widget.currentText()

    def get_value(self) -> int:
        """
        get value of option.\n
        :return: return value of option
        """
        return self.widget.currentIndex()

    def set_value(self, value: int) -> None:
        """
        set value of option.\n
        :param value: value to be set
        """
        self.widget.setCurrentIndex(value)

    def _init_links(self) -> None:
        """
        Set way on which the links should be set\n
        """
        current_value: int = self.get_value()
        self.set_value(0 if current_value != 0 else 1)
        self.set_value(current_value)

    def _check_value(self) -> bool:
        return self.widget.currentIndex() >= 0

    def set_text(self, name: str):
        entry_name: List[str, str] = name.split(',')
        self.label_text = entry_name[0]
        self.label.setText(self.label_text)
        for idx, name in enumerate(entry_name[1:]):
            self.widget.setItemText(idx, name)

    def add_link_2_show(self, option: Union[Option, Category, FunctionButton, Hint], *, on_index: int):
        """
        Add link to the index\n
        :param option: option which should be linked
        :param on_index: index on which the option should be shown
        """
        self.linked_options.append([option, on_index])

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        Function for the change event\n
        :param function_to_be_called: function to be called if option has changed
        """
        self.widget.currentIndexChanged.connect(function_to_be_called)  # pylint: disable=E1101

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout, *, row: int = None, column: int = None) -> None:
        layout = self.create_frame(frame, layout_parent)
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f"QFrame {'{'}border: 1px solid {WHITE};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}"
            f"QComboBox{'{'}border: 1px solid {WHITE};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}"
        )
        self.widget.addItems(self.entries)
        self.widget.setCurrentIndex(self.default_value)
        self.widget.setMaximumWidth(100)
        self.widget.setMinimumWidth(100)
        self.widget.currentIndexChanged.connect(ft_partial(check, self.linked_options, self))  # pylint: disable=E1101
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.widget, column, row)
            return
        layout.addWidget(self.widget)


class FileNameBox(Option):
    """
    Filename input box\n
    """
    def __init__(self, label: str,default_value: str, *, dialog_text: str, error_text: str, status_bar: QtW.QStatusBar,category: Category):
        super().__init__(label, default_value, category)
        self.widget: QtW.QLineEdit = QtW.QLineEdit(self.default_parent)
        self.dialog_text: str = dialog_text
        self.error_text: str = error_text
        self.status_bar: QtW.QStatusBar = status_bar

    def get_value(self) -> str:
        """
        get value of option.\n
        :return: return value of option
        """
        return self.widget.text()

    def set_value(self, value: str) -> None:
        """
        set value of option.\n
        :param value: value to be set
        """
        self.widget.setText(value)

    def _init_links(self) -> None:
        """
        Set way on which the links should be set\n
        """
        current_value: str = self.get_value()
        self.set_value('test')
        self.set_value(current_value)

    def _check_value(self) -> bool:
        return exists(self.widget.text())

    def change_event(self, function_to_be_called: Callable) -> None:
        """
        Function for the change event\n
        :param function_to_be_called: function to be called if option has changed
        """
        self.widget.textChanged.connect(function_to_be_called)  # pylint: disable=E1101

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout, *, row: int = None, column: int = None) -> None:
        layout = self.create_frame(frame, layout_parent, False)
        self.widget.setParent(self.frame)
        self.widget.setStyleSheet(
            f"QLineEdit{'{'}border: 3px solid {LIGHT};border-radius: 5px;color: {WHITE};gridline-color: {LIGHT};background-color: {LIGHT};font-weight:500;\n"
            f"selection-background-color: {LIGHT_SELECT};{'}'}\n"
            f"QLineEdit:hover{'{'}background-color: {DARK};{'}'}"
        )
        layout.addWidget(self.widget)
        button = QtW.QPushButton(self.frame)
        button.setMinimumSize(QtC.QSize(30, 30))
        button.setMaximumSize(QtC.QSize(30, 30))
        button.setText("...")
        button.clicked.connect(self.fun_choose_file)  # pylint: disable=E1101
        layout.addWidget(button)

    def fun_choose_file(self) -> None:
        """
        function to choose data file Import
        :return: None
        """
        # try to ask for a file otherwise show message in status bar
        try:
            filename = QtW.QFileDialog.getOpenFileName(self.frame, caption=self.dialog_text, filter="(*.csv)")
            self.widget.setText(filename[0])
        # show warning if no file is selected in status bar for 5 seconds
        except FileNotFoundError:
            self.status_bar.showMessage(self.error_text, 5000)


class Hint:
    """
    Hint class to add hint texts in categories\n
    """

    default_parent: Optional[QtW.QWidget] = None

    def __init__(self, hint: str, category: Category, warning: bool = False):
        self.hint: str = hint
        self.label: QtW.QLabel = QtW.QLabel(self.default_parent)
        self.warning = warning
        category.list_of_options.append(self)

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout, *, row: int = None, column: int = None) -> None:
        self.label.setParent(frame)
        self.label.setText(self.hint)
        if self.warning:
            self.label.setStyleSheet(f"color: {WARNING};")
        self.label.setWordWrap(True)
        if row is not None and isinstance(layout_parent, QtW.QGridLayout):
            layout_parent.addWidget(self.label, column, row)
            return
        layout_parent.addWidget(self.label)

    def hide(self) -> None:
        self.label.hide()

    def show(self) -> None:
        self.label.show()

    def is_hidden(self) -> bool:
        return self.label.isHidden()

    def set_text(self, name: str):
        self.hint: str = name
        self.label.setText(self.hint)


class FunctionButton:
    """
    Function button to link function to\n
    """
    default_parent: Optional[QtW.QWidget] = None

    def __init__(self, button_text: str, icon: str, category: Category):
        self.button_text: str = button_text
        self.icon: str = icon
        self.frame: QtW.QFrame = QtW.QFrame(self.default_parent)
        self.button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        category.list_of_options.append(self)

    def create_widget(self, frame: QtW.QFrame, layout_parent: QtW.QLayout):
        self.button.setParent(frame)
        self.button.setText(f"  {self.button_text}  ")
        icon = QtG.QIcon()
        # icon11.addPixmap(QtGui_QPixmap(icon), QtGui_QIcon.Normal, QtGui_QIcon.Off)
        icon.addFile(self.icon)
        self.button.setIcon(icon)
        self.button.setIconSize(QtC.QSize(20, 20))
        self.button.setMinimumWidth(100)
        self.button.setMinimumHeight(35)
        self.frame.setParent(frame)
        self.frame.setFrameShape(QtW.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtW.QFrame.Raised)
        self.frame.setStyleSheet(f"QFrame{'{'}border: 0px solid {WHITE};border-radius: 0px;{'}'}")
        layout = QtW.QHBoxLayout(self.frame)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        spacer1 = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        layout.addItem(spacer1)

        layout.addWidget(self.button)
        spacer2 = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)
        layout.addItem(spacer2)

        layout_parent.addWidget(self.frame)

    def hide(self) -> None:
        self.frame.hide()

    def show(self) -> None:
        self.frame.show()

    def is_hidden(self) -> bool:
        return self.frame.isHidden()

    def set_text(self, name: str):
        self.button_text: str = name
        self.button.setText(self.button_text)

    def change_event(self, function_to_be_called: Callable, *args) -> None:
        """
        Function for the change event\n
        :param function_to_be_called: function to be called if option has changed
        """
        self.button.clicked.connect(lambda: function_to_be_called(*args))


class ResultText(Hint):

    def __init__(self, result_name: str, category: Category, prefix: str = "", suffix: str = ""):
        super().__init__(result_name, category, warning=False)
        self.class_name: str = ""
        self.var_name: str = ""
        self.prefix: str = prefix
        self.suffix: str = suffix
        self._callable = lambda x: str(x)

    def text_to_be_shown(self, class_name: str = "Borefield", var_name: str = "H") -> None:
        self.class_name = class_name
        self.var_name = var_name

    def function_to_convert_to_text(self, function) -> None:
        self._callable = function

    def set_text(self, data) -> None:
        super().set_text(self.prefix + str(self._callable(data)) + self.suffix)


class Category:
    """
    Category which consists of options\n
    """

    default_parent: Optional[QtW.QWidget] = None

    def __init__(self, label: str, page: Page):
        self.label_text: str = label
        self.label: QtW.QLabel = QtW.QLabel(self.default_parent)
        self.list_of_options: List[Union[Option, Hint, FunctionButton]] = []
        self.frame: QtW.QFrame = QtW.QFrame(self.default_parent)
        self.graphic_left: Optional[Union[QtW.QGraphicsView, bool]] = None
        self.graphic_right: Optional[Union[QtW.QGraphicsView, bool]] = None
        self.grid_layout: int = 0
        self.layout_frame: Optional[QtW.QVBoxLayout] = None
        page.list_categories.append(self)
        self.options_hidden = []

    def activate_graphic_left(self):
        self.graphic_left = True

    def activate_graphic_right(self):
        self.graphic_right = True

    def activate_grid_layout(self, column: int):
        self.grid_layout = column

    def set_text(self, name: str):
        self.label_text = name
        self.label.setText(name)

    def create_widget(self, page: QtW.QWidget, layout: QtW.QLayout):
        self.label.setParent(page)
        self.label.setText(self.label_text)
        self.label.setStyleSheet(
            f"QLabel {'{'}border: 1px solid  {LIGHT};border-top-left-radius: 15px;border-top-right-radius: 15px;background-color:  {LIGHT};padding: 5px 0px;\n"
            f"	color:  {WHITE};font-weight:500;{'}'}"
        )
        self.label.setAlignment(QtC.Qt.AlignCenter | QtC.Qt.AlignVCenter)
        layout.addWidget(self.label)
        self.frame.setParent(page)
        self.frame.setStyleSheet(
            f"QFrame{'{'}border: 1px solid {LIGHT};border-bottom-left-radius: 15px;border-bottom-right-radius: 15px;{'}'}\n"
            f"QLabel{'{'}border: 0px solid {WHITE};{'}'}"
        )
        self.frame.setFrameShape(QtW.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtW.QFrame.Raised)
        layout.addWidget(self.frame)
        spacer_label = QtW.QLabel(page)
        spacer_label.setMinimumHeight(6)
        spacer_label.setMaximumHeight(6)
        layout.addWidget(spacer_label)
        layout_frame_horizontal = QtW.QHBoxLayout(self.frame)
        if self.graphic_left is not None:
            self.graphic_left = self.create_graphic_view(layout_frame_horizontal)
        if self.grid_layout > 0:
            self.layout_frame = QtW.QGridLayout(self.frame)
            row = 0
            column = 0
            for option in self.list_of_options:
                if isinstance(option, Hint):
                    option.create_widget(self.frame, self.layout_frame, row=row, column=column)
                else:
                    if option.label_text == "":
                        option.deactivate_size_limit()
                    option.create_widget(self.frame, self.layout_frame, row=row, column=column)
                if row == self.grid_layout - 1:
                    row = 0
                    column += 1
                    continue
                row += 1
        else:
            self.layout_frame = QtW.QVBoxLayout(self.frame)
            for option in self.list_of_options:
                option.create_widget(self.frame, self.layout_frame)

        layout_frame_horizontal.addLayout(self.layout_frame)

        if self.graphic_right is not None:
            self.graphic_right = self.create_graphic_view(layout_frame_horizontal)

    def create_graphic_view(self, layout: QtW.QLayout) -> QtW.QGraphicsView:
        graphic_view = QtW.QGraphicsView(self.frame)
        graphic_view.setMinimumSize(QtC.QSize(0, 0))
        graphic_view.setMaximumSize(QtC.QSize(100, 16777215))
        graphic_view.setStyleSheet(
            f"QFrame{'{'}border: 1px solid {LIGHT};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}\n"
            f"QLabel{'{'}border: 0px solid {WHITE};{'}'}"
        )

        layout.addWidget(graphic_view)
        return graphic_view

    def hide(self, **kwargs) -> None:
        self.frame.hide()
        self.label.hide()
        for option in self.list_of_options:
            # only hide the options that were not already hidden
            # this since otherwise there can be problems with options at the results page
            if option.is_hidden():
                continue
            self.options_hidden.append(option)
            option.hide()

    def show(self, **kwargs) -> None:
        self.frame.show()
        self.label.show()
        for option in self.options_hidden:
            option.show()
        self.options_hidden = []

    def is_hidden(self) -> bool:
        return self.frame.isHidden()


class FigureOption(ButtonBox):

    def __init__(self, category, label, param, default, entries, entries_values):
        super(FigureOption, self).__init__(label=label, default_index=default, entries=entries, category=category)
        self.values = entries_values
        self.param = param

    def get_value(self) -> Tuple[str, int]:
        for idx, button in enumerate(self.widget):
            if button.isChecked():
                return self.param, self.values[idx]
        return "", -1

    def set_value(self, values: Tuple[str, int]):
        value = values[1]
        for idx, button in enumerate(self.widget):
            if self.values[idx] == value:
                if not button.isChecked():
                    button.click()
                break
        return


class ResultFigure(Category):

    def __init__(self, label: str, page, save_figure_button: bool = True):

        super().__init__(label, page)
        self.fig = None
        self.ax = None
        self.canvas = None
        self.save_fig: bool = False
        self._kwargs: dict = {}
        self.function_name: str = ""
        self.class_name: str = ""
        self.to_show: bool = True

        if save_figure_button:
            self.save_fig = FunctionButton(category=self, button_text="Save figure", icon=":/icons/icons/Save_Inv.svg")

    def fig_to_be_shown(self, class_name: str = "Borefield", function_name: str = "print_temperature_profile", **kwargs):
        self.class_name = class_name
        self.function_name = function_name
        self._kwargs = kwargs

    @property
    def kwargs(self):
        kwargs_temp = {}
        for i in self.list_of_options:
            if i != self.save_fig and not i.is_hidden():
                key, value = i.get_value()
                kwargs_temp[key] = value
        # try:
        #     # works only in python 3.9 and higher
        #     return self._kwargs | kwargs_temp
        # except TypeError:
        #     temp = {**self._kwargs, **kwargs_temp}
        #     print(temp)
        return {**self._kwargs, **kwargs_temp}

    def options_to_show(self, label: str, param: str, default_index: int, entries_text: List[str], entries_values: List) -> None:
        self.options.append(FigureOption(category=self, param=param, label=label, default=default_index,
                                         entries=entries_text, entries_values=entries_values))

    def show(self, results: bool = False) -> None:
        if self.to_show:
            super(ResultFigure, self).show()
        if results:
            return
        self.to_show = True

    def hide(self, results: bool = False) -> None:
        super(ResultFigure, self).hide()
        if results:
            return
        self.to_show = False


class Aim:
    """
    Aim of simulation\n
    """

    default_parent: Optional[QtW.QWidget] = None

    def __init__(self, label: str, icon: str, page: Page):
        self.label: str = label
        self.icon: str = icon
        self.widget: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        self.list_options: List[Union[Option, Category, FunctionButton]] = []
        page.upper_frame.append(self)

    def change_event(self, function_to_be_called: Callable, *args) -> None:
        """
        Function for the change event\n
        :param function_to_be_called: function to be called if option has changed
        """
        self.widget.clicked.connect(lambda: function_to_be_called(*args))  # pylint: disable=E1101

    def add_link_2_show(self, option: Union[Option, Category, FunctionButton, Hint]):
        """
        Add link to the aim\n
        :param option: option which should be linked
        """
        self.list_options.append(option)

    def create_widget(self, frame: QtW.QFrame, layout: QtW.QGridLayout, idx: int) -> None:
        icon11 = QtG.QIcon()
        # icon11.addPixmap(QtGui_QPixmap(icon), QtGui_QIcon.Normal, QtGui_QIcon.Off)
        icon11.addFile(self.icon)
        self.widget.setParent(frame)
        push_button = self.widget
        push_button.setIcon(icon11)
        push_button.setMinimumSize(QtC.QSize(0, 60))
        push_button.setMaximumSize(QtC.QSize(16777215, 60))
        push_button.setStyleSheet(
            f"QPushButton{'{'}border: 3px solid {DARK};border-radius: 15px;color:{WHITE};gridline-color: {LIGHT};background-color: {GREY};font-weight:500;{'}'}"
            f"QPushButton:hover{'{'}border: 3px solid {DARK};background-color:{LIGHT};{'}'}"
            f"QPushButton:checked{'{'}border:3px solid {LIGHT};background-color:{LIGHT};{'}'}\n"
            f"QPushButton:disabled{'{'}border: 3px solid {GREY};border-radius: 5px;color: {WHITE};gridline-color: {GREY};background-color: {GREY};{'}'}\n"
            f"QPushButton:disabled:hover{'{'}background-color: {DARK};{'}'}"
        )
        # push_button.setIcon(icon11)
        # push_button.setIcon(QtGui_QIcon(QtGui_QPixmap(icon)))
        push_button.setIconSize(QtC.QSize(30, 30))
        push_button.setCheckable(True)
        push_button.setText(self.label)
        layout.addWidget(push_button, int(idx / 2), 0 if divmod(idx, 2)[1] == 0 else 1, 1, 1)


def check_aim_options(list_aim: List[Aim]):
    list_false = [aim for aim in list_aim if not aim.widget.isChecked()]
    list_true = [aim for aim in list_aim if aim.widget.isChecked()]
    for aim in list_false:
        for option in aim.list_options:
            if isinstance(option, list):
                for opt in option:
                    opt.hide()
                continue
            option.hide()
    for aim in list_true:
        for option in aim.list_options:
            if isinstance(option, list):
                for opt in option:
                    opt.show()
                continue
            option.show()


class Page:
    """
    Page which consists of aim and categories\n
    """
    next_label: str = 'next'
    previous_label: str = 'previous'
    default_parent: Optional[QtW.QWidget] = None
    TOGGLE: bool = True

    def __init__(self, name: str, button_name: str, icon: str):
        self.name: str = name
        self.button_name: str = button_name
        self.icon: str = icon
        self.push_button_next: Optional[QtW.QPushButton] = None
        self.push_button_previous: Optional[QtW.QPushButton] = None
        self.list_categories: List[Category] = []
        self.button: QtW.QPushButton = QtW.QPushButton(self.default_parent)
        self.label: QtW.QLabel = QtW.QLabel(self.default_parent)
        self.label_gap: QtW.QLabel = QtW.QLabel(self.default_parent)
        self.page: QtW.QWidget = QtW.QWidget(self.default_parent)
        self.previous_page: Optional[Page] = None
        self.next_page: Optional[Page] = None
        self.upper_frame: List[Union[Aim, Option, Category]] = []
        self.functions_button_clicked: List[Callable] = []

    def add_function_called_if_button_clicked(self, function_2_be_called: Callable):
        self.functions_button_clicked.append(function_2_be_called)

    def set_text(self, name: str):
        entry_name: List[str, str] = name.split(',')
        self.name = entry_name[1]
        self.button_name = entry_name[0].replace('@', '\n')
        self.label.setText(self.name)
        self.button.setText(self.button_name)
        if self.push_button_previous is not None:
            self.push_button_previous.setText(self.previous_label)
        if self.push_button_next is not None:
            self.push_button_next.setText(self.next_label)

    def set_previous_page(self, previous_page: Page):
        self.previous_page = previous_page

    def set_next_page(self, next_page: Page):
        self.next_page = next_page

    def set_upper_frame(self, options: List[Union[Aim, Option, Category]]):
        self.upper_frame: List[Union[Aim, Option, Category]] = options

    def create_page(self, central_widget: QtW.QWidget, stacked_widget: QtW.QStackedWidget, vertical_layout_menu: QtW.QVBoxLayout):
        self.page.setParent(central_widget)
        layout = QtW.QVBoxLayout(self.page)
        layout.setSpacing(0)
        self.label.setParent(central_widget)
        label: QtW.QLabel = self.label
        label.setStyleSheet('font: 63 16pt "Lexend SemiBold";')
        label.setText(self.name)
        layout.addWidget(label)
        spacer_label = QtW.QLabel(self.page)
        spacer_label.setMinimumHeight(6)
        spacer_label.setMaximumHeight(6)
        layout.addWidget(spacer_label)
        scroll_area = QtW.QScrollArea(self.page)
        scroll_area.setFrameShape(QtW.QFrame.NoFrame)
        scroll_area.setLineWidth(0)
        scroll_area.setWidgetResizable(True)
        scroll_area_content = QtW.QWidget(self.page)
        scroll_area_content.setGeometry(QtC.QRect(0, 0, 864, 695))
        scroll_area.setWidget(scroll_area_content)
        layout.addWidget(scroll_area)
        scroll_area_layout = QtW.QVBoxLayout(scroll_area_content)
        scroll_area_layout.setSpacing(0)
        scroll_area_layout.setContentsMargins(0, 0, 0, 0)
        stacked_widget.addWidget(self.page)
        if self.upper_frame:
            self.create_upper_frame(scroll_area_content, scroll_area_layout)
        label_gap = QtW.QLabel(central_widget)
        label_gap.setMinimumSize(QtC.QSize(0, 6))
        label_gap.setMaximumSize(QtC.QSize(16777215, 6))

        scroll_area_layout.addWidget(label_gap)

        for category in self.list_categories:
            category.create_widget(scroll_area_content, scroll_area_layout)

        spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Expanding)
        scroll_area_layout.addItem(spacer)

        self.create_links_to_other_pages(central_widget, layout)

        self.button.setParent(central_widget)
        self.button.setMinimumSize(QtC.QSize(100, 100))
        icon23 = QtG.QIcon()
        icon23.addFile(self.icon, QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)
        self.button.setIcon(icon23)
        self.button.setIconSize(QtC.QSize(24, 24))
        self.button.setText(self.button_name)
        self.label_gap.setParent(central_widget)
        self.label_gap.setMinimumSize(QtC.QSize(0, 6))
        self.label_gap.setMaximumSize(QtC.QSize(16777215, 6))

        vertical_layout_menu.addWidget(self.button)
        vertical_layout_menu.addWidget(self.label_gap)
        self.button.clicked.connect(ft_partial(stacked_widget.setCurrentWidget, self.page))  # pylint: disable=E1101
        for function_2_be_called in self.functions_button_clicked:
            self.button.clicked.connect(function_2_be_called)  # pylint: disable=E1101

    def create_upper_frame(self, scroll_area_content: QtW.QWidget, scroll_area_layout: QtW.QVBoxLayout):
        """
        create the upper frame\n
        :param scroll_area_content:
        :param scroll_area_layout:
        """
        upper_frame = QtW.QFrame(scroll_area_content)
        upper_frame.setStyleSheet(
            f"QFrame {'{'}border: 1px solid {LIGHT};border-top-left-radius: 15px;border-top-right-radius: 15px;"
            f"border-bottom-left-radius: 15px;border-bottom-right-radius: 15px;{'}'}\n"
            f"QLabel{'{'}border: 0px solid {WHITE};{'}'}"
        )
        upper_frame.setFrameShape(QtW.QFrame.StyledPanel)
        upper_frame.setFrameShadow(QtW.QFrame.Raised)
        upper_frame.setSizePolicy(QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Minimum)
        grid_layout = QtW.QGridLayout(upper_frame)
        grid_layout.setVerticalSpacing(6)
        grid_layout.setHorizontalSpacing(6)
        scroll_area_layout.addWidget(upper_frame)
        for idx, option in enumerate(self.upper_frame):
            if isinstance(option, Aim):
                option.create_widget(upper_frame, grid_layout, idx)
                continue
            option.create_widget(upper_frame, grid_layout)

        list_aims: List[Aim] = [aim for aim in self.upper_frame if isinstance(aim, Aim)]
        if list_aims:
            for idx, aim in enumerate(list_aims):
                default_value = 1 if idx == 0 else 0
                aim.widget.clicked.connect(
                    ft_partial(self.update_function, aim.widget, list_aims[default_value].widget,
                               [aim.widget for i, aim in enumerate(list_aims) if i not in [idx, default_value]])
                )  # pylint: disable=E1101
                aim.widget.clicked.connect(ft_partial(check_aim_options, list_aims))  # pylint: disable=E1101
            list_aims[0].widget.click()

    def update_function(self, button: QtW.QPushButton, button_opponent: QtW.QPushButton, false_button_list: List[QtW.QPushButton] = None):
        if self.TOGGLE:
            _update_opponent_toggle(button, button_opponent, false_button_list)
            return
        _update_opponent_not_change(button, false_button_list + [button_opponent])

    def create_links_to_other_pages(self, central_widget: QtW.QWidget, scroll_area_layout: QtW.QVBoxLayout):
        """
        create link on the bottom to other pages.\n
        :param central_widget: central widget
        :param scroll_area_layout: scroll area layout
        """
        if self.previous_page is None and self.next_page is None:
            return

        horizontal_layout = QtW.QHBoxLayout(scroll_area_layout.parent())

        if self.previous_page is not None:
            self.push_button_previous = QtW.QPushButton(central_widget)
            self.push_button_previous.setMinimumSize(QtC.QSize(0, 30))
            self.push_button_previous.setMaximumSize(QtC.QSize(16777215, 30))
            icon = QtG.QIcon()
            icon.addFile(":/icons/icons/ArrowLeft2.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)
            self.push_button_previous.setIcon(icon)
            self.push_button_previous.setIconSize(QtC.QSize(20, 20))
            self.push_button_previous.setText(f"  {self.previous_label}  ")

            horizontal_layout.addWidget(self.push_button_previous)
            self.push_button_previous.clicked.connect(self.previous_page.button.click)  # pylint: disable=E1101

        horizontal_spacer = QtW.QSpacerItem(1, 1, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)

        horizontal_layout.addItem(horizontal_spacer)
        if self.next_page is not None:
            self.push_button_next = QtW.QPushButton(central_widget)
            self.push_button_next.setMinimumSize(QtC.QSize(0, 30))
            self.push_button_next.setMaximumSize(QtC.QSize(16777215, 30))
            self.push_button_next.setLayoutDirection(QtC.Qt.RightToLeft)
            icon = QtG.QIcon()
            icon.addFile(":/icons/icons/ArrowRight2.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)
            self.push_button_next.setIcon(icon)
            self.push_button_next.setIconSize(QtC.QSize(20, 20))
            self.push_button_next.setText(f"  {self.next_label}  ")

            horizontal_layout.addWidget(self.push_button_next)
            self.push_button_next.clicked.connect(self.next_page.button.click)  # pylint: disable=E1101

        scroll_area_layout.addLayout(horizontal_layout)
