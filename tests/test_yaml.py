from munch import Munch


def test_from_yaml(yaml):
    data = yaml.load('''
    Flow style: !munch.Munch { Clark: Evans, Brian: Ingerson, Oren: Ben-Kiki }
    Block style: !munch
      Clark : Evans
      Brian : Ingerson
      Oren  : Ben-Kiki
    ''')
    assert data == {
        'Flow style': Munch(Brian='Ingerson', Clark='Evans', Oren='Ben-Kiki'),
        'Block style': Munch(Brian='Ingerson', Clark='Evans', Oren='Ben-Kiki'),
    }


def test_to_yaml_safe(yaml):
    b = Munch(foo=['bar', Munch(lol=True)], hello=42)
    dumped = yaml.safe_dump(b, default_flow_style=True)
    assert dumped == '{foo: [bar, {lol: true}], hello: 42}\n'


def test_to_yaml(yaml):
    b = Munch(foo=['bar', Munch(lol=True)], hello=42)
    dumped = yaml.dump(b, default_flow_style=True)
    assert dumped == '!munch.Munch {foo: [bar, !munch.Munch {lol: true}], hello: 42}\n'


def test_toYAML(yaml):
    b = Munch(foo=['bar', Munch(lol=True)], hello=42)
    assert yaml.safe_dump(b, default_flow_style=True) == '{foo: [bar, {lol: true}], hello: 42}\n'
    assert b.toYAML(default_flow_style=True) == '{foo: [bar, {lol: true}], hello: 42}\n'
    assert yaml.dump(b, default_flow_style=True) == '!munch.Munch {foo: [bar, !munch.Munch {lol: true}], hello: 42}\n'
    assert b.toYAML(Dumper=yaml.Dumper, default_flow_style=True) == \
        '!munch.Munch {foo: [bar, !munch.Munch {lol: true}], hello: 42}\n'
